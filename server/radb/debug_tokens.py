from antlr4 import *
from radb.RALexer import RALexer

# The query causing the issue
query = r"\pi_{name, balance} (RichSavers);"

print(f"--- Tokenizing: {query} ---")

input_stream = InputStream(query)
lexer = RALexer(input_stream)
token = lexer.nextToken()

while token.type != Token.EOF:
    # Get the symbolic name (e.g., 'PI', 'ID', 'ARG_R')
    rule_name = lexer.symbolicNames[token.type]
    print(f"Token: {token.text.ljust(15)} | Type: {rule_name}")
    token = lexer.nextToken()