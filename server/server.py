import io
import os
import contextlib
import configparser
from flask import Flask, request, jsonify
from flask_cors import CORS
import re

# Import ANTLR components for parsing scripts
from antlr4 import InputStream, CommonTokenStream

# Import radb modules
import radb.db
import radb.typesys
from radb.ast import Context
from radb.views import ViewCollection
from radb.RALexer import RALexer
from radb.RAParser import RAParser
from radb.parse import RAErrorListener, ASTBuilder

app = Flask(__name__)
CORS(app)

# --- Load Defaults ---
sys_config_path = os.path.join(os.path.dirname(radb.__file__), 'sys.ini')
sys_config = configparser.ConfigParser()
sys_config.read(sys_config_path)
DEFAULT_FUNCTIONS = sys_config.get('DEFAULT', 'default_functions', fallback='')

# --- DB Config ---
DB_CONFIG = {
    'db.drivername': 'sqlite+pysqlite',
    'db.database': 'bank.db', 
    'default_functions': DEFAULT_FUNCTIONS,
    'functions': ''
}

# --- Initialize Context ---
try:
    print("Connecting to database...")
    db_inst = radb.db.DB(DB_CONFIG)
    check = radb.typesys.ValTypeChecker(
        DB_CONFIG['default_functions'], 
        DB_CONFIG.get('functions', None)
    )
    # The ViewCollection persists between requests
    ra_context = Context(DB_CONFIG, db_inst, check, ViewCollection())
    print("Database connected successfully.")
except Exception as e:
    print(f"Failed to initialize DB: {e}")
    exit(1)

def clean_query(raw_query):
    """
    Pre-processes the raw LaTeX input to fix frontend artifacts and convert syntax.
    """
    if not raw_query:
        return ""
    
    clean = raw_query
    
    # 1. Fix Underscores (frontend sends \text{_})
    clean = clean.replace(r'\text{_}', '_')

    # 2. Convert Grouping Gamma: {}_{cols} \gamma_{aggrs}  ->  \gamma_{cols: aggrs}
    # Pattern explanation:
    # \{ *\}        Matches the empty group {}
    # *\_ *\{       Matches the subscript start _{
    # ([^\}]+)      Captures the grouping columns (group 1)
    # \}            Matches closing brace }
    # *\\gamma      Matches \gamma
    # *\_ *\{       Matches the second subscript start _{
    # ([^\}]+)      Captures the aggregation expressions (group 2)
    # \}            Matches closing brace }
    
    # Note: We use a non-greedy approach or simple logic assuming no nested braces for now.
    clean = re.sub(
        r"\{ *\} *\_ *\{([^\}]+)\} *\\gamma *\_ *\{([^\}]+)\}", 
        r"\\gamma_{\1: \2}", 
        clean
    )

    # 3. Ensure Semicolon
    if not clean.strip().endswith(';') and '\n' not in clean:
        clean += ';'
        
    return clean

def parse_full_script(script_text):
    """
    Parses a string containing multiple RA statements (separated by ;)
    Returns a list of AST nodes.
    """
    lexer = RALexer(InputStream(script_text))
    lexer._listeners = [RAErrorListener()]
    parser = RAParser(CommonTokenStream(lexer))
    parser._listeners = [RAErrorListener()]
    
    # parser.program() handles "(statement)* EOF"
    tree = parser.program() 
    
    # Visitor returns a list of ASTs for 'program' rule
    return ASTBuilder().visit(tree)

@app.route('/run', methods=['POST'])
def run_query():
    data = request.json
    raw_query = data.get('query', '').strip()

    if not raw_query:
        return jsonify({'error': 'Empty query'}), 400

    # --- Clean the Input ---
    query = clean_query(raw_query)

    output_capture = io.StringIO()
    
    try:
        with contextlib.redirect_stdout(output_capture):
            # 1. Parse the entire script (multiple statements)
            statements = parse_full_script(query)
            
            # 2. Execute them in order
            for i, ast in enumerate(statements):
                if len(statements) > 1:
                    print(f"--- Step {i+1} ---")
                
                ast.validate(ra_context)
                ast.execute(ra_context)
            
        return jsonify({
            'status': 'success',
            'output': output_capture.getvalue()
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, port=5001)