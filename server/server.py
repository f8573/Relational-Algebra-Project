import io
import os
import contextlib
import configparser
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import radb modules
import radb.db
import radb.parse
import radb.typesys
from radb.ast import Context
from radb.views import ViewCollection

app = Flask(__name__)
CORS(app)

# --- Load System Configuration ---
# We need to read the default functions (PLUS, MINUS, etc.) from sys.ini
# just like the main library does.
sys_config_path = os.path.join(os.path.dirname(radb.__file__), 'sys.ini')
sys_config = configparser.ConfigParser()
sys_config.read(sys_config_path)

# Extract the big string of default function definitions
DEFAULT_FUNCTIONS = sys_config.get('DEFAULT', 'default_functions', fallback='')

# --- Database Configuration ---
DB_CONFIG = {
    'db.drivername': 'sqlite+pysqlite',
    'db.database': 'bank.db', 
    'default_functions': DEFAULT_FUNCTIONS, # Pass the string we just loaded
    'functions': ''
}

# --- Initialize RADB Context ---
try:
    print("Connecting to database...")
    db_inst = radb.db.DB(DB_CONFIG)
    
    # Initialize the type checker with the loaded defaults
    check = radb.typesys.ValTypeChecker(
        DB_CONFIG['default_functions'], 
        DB_CONFIG.get('functions', None)
    )
    
    # Create the global context
    ra_context = Context(DB_CONFIG, db_inst, check, ViewCollection())
    print("Database connected successfully.")

except Exception as e:
    print(f"Failed to initialize DB: {e}")
    exit(1)

@app.route('/run', methods=['POST'])
def run_query():
    data = request.json
    raw_query = data.get('query', '').strip()

    if not raw_query:
        return jsonify({'error': 'Empty query'}), 400

    if not raw_query.endswith(';'):
        raw_query += ';'

    output_capture = io.StringIO()
    
    try:
        with contextlib.redirect_stdout(output_capture):
            ast = radb.parse.one_statement_from_string(raw_query)
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
    app.run(debug=True, port=5000)