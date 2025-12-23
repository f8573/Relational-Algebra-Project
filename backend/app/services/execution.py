"""RA execution utilities.

Provides `RAExecutor` — helper to parse and execute RA scripts.
Uses the bundled `radb` engine. Each call creates a fresh execution
context to isolate runs and capture stdout.
"""

import io
import os
import contextlib
import configparser
import re

from antlr4 import InputStream, CommonTokenStream

# Import radb modules
import radb
import radb.db
import radb.typesys
from radb.ast import Context
from radb.views import ViewCollection
from radb.RALexer import RALexer
from radb.RAParser import RAParser
from radb.parse import RAErrorListener, ASTBuilder


class RAExecutor:
    def __init__(self, db_path='bank.db'):
        """Create an executor bound to a particular database.

        Args:
            db_path: path to an sqlite `.db` file or a SQLAlchemy URL. If the
                string ends with `.db` it is treated as a sqlite filename;
                otherwise it will be passed through as a SQLAlchemy URL.
        """
        self.db_path = db_path
        self.default_functions = self._load_defaults()

    def _load_defaults(self):
        """Load radb default function signatures from the packaged `sys.ini`.

        Returns the raw `default_functions` string or an empty string if the
        configuration cannot be read.
        """
        try:
            sys_config_path = os.path.join(
                os.path.dirname(radb.__file__), 'sys.ini')
            sys_config = configparser.ConfigParser()
            sys_config.read(sys_config_path)
            return sys_config.get('DEFAULT', 'default_functions', fallback='')
        except Exception:
            # Fallback if radb isn't installed in a standard way
            return ''

    def _clean_query(self, raw_query):
        """Pre-process frontend RA input to remove common artifacts.

        Transformations are intentionally small and reversible: replace
        `\text{_}` with `_`, normalize a small gamma grouping pattern, and
        ensure a trailing semicolon on single-line queries.

        Args:
            raw_query: the raw text received from the frontend.

        Returns:
            A cleaned string ready for parsing.
        """
        if not raw_query:
            return ""

        clean = raw_query

        # 1. Fix underscores emitted as \text{_}
        clean = clean.replace(r"\text{_}", "_")

        # 2. Convert grouping gamma patterns to a compact form.
        pattern = (
            r"(?:\\text\{ *\\}|\{ *\}) *\\_ *\{([^\}]+)\}"
            r" *\\gamma *\\_ *\{([^\}]+)\}"
        )
        clean = re.sub(pattern, r"\\gamma_{\1: \2}", clean)

        # 3. Ensure semicolon for single-line queries
        if not clean.strip().endswith(";") and "\n" not in clean:
            clean += ";"

        return clean

    def _parse_full_script(self, script_text):
        """Parse a script containing one or more RA statements and return ASTs.

        Returns a list of AST nodes produced by `ASTBuilder`.
        """
        lexer = RALexer(InputStream(script_text))
        lexer._listeners = [RAErrorListener()]
        parser = RAParser(CommonTokenStream(lexer))
        parser._listeners = [RAErrorListener()]

        tree = parser.program()
        return ASTBuilder().visit(tree)

    def execute(self, raw_query):
        """Execute a relational-algebra script and capture its output.

        Builds a fresh radb `Context` for each call. The context includes
        DB configuration, a type checker and view collection to avoid
        cross-request state. Captured stdout is returned as the first
        tuple element; on exception the second element contains the
        error message.

        Args:
            raw_query: RA script to execute.

        Returns:
            (output: str, error: Optional[str])
        """
        # Configure DB for this specific run
        # Construct db_config based on whether db_path looks like a file
        if isinstance(self.db_path, str) and self.db_path.endswith('.db'):
            db_config = {
                'db.drivername': 'sqlite+pysqlite',
                'db.database': self.db_path,
                'default_functions': self.default_functions,
                'functions': ''
            }
        else:
            # Assume SQLAlchemy URL or similar
            db_config = {
                'db.drivername': 'sqlalchemy',
                'db.database': self.db_path,
                'default_functions': self.default_functions,
                'functions': ''
            }

        output_capture = io.StringIO()

        try:
            # Initialize fresh context for isolation
            db_inst = radb.db.DB(db_config)
            check = radb.typesys.ValTypeChecker(
                db_config["default_functions"],
                db_config.get("functions", None),
            )
            ra_context = Context(db_config, db_inst, check, ViewCollection())

            # Clean and Parse
            query = self._clean_query(raw_query)

            # Capture stdout
            with contextlib.redirect_stdout(output_capture):
                statements = self._parse_full_script(query)

                for i, ast in enumerate(statements):
                    if len(statements) > 1:
                        print(f"--- Step {i+1} ---")

                    ast.validate(ra_context)
                    ast.execute(ra_context)

            return output_capture.getvalue(), None

        except Exception as e:
            return output_capture.getvalue(), str(e)
