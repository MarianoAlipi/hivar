from lexer_parser import lexer, parser
from file_manager import get_file_content
from structures.symbol_table import SymbolTable

DEBUG_MODE = 0

lines = get_file_content("tests/input.txt")
lexer.input(lines)

try:
    print('Parsing...')
    parser.parse(lines, debug=DEBUG_MODE)
    print('Correct syntax.')
except SyntaxError as e:
    print(f'Syntax error: unexpected {e.args[0]}')

if DEBUG_MODE:
    st = SymbolTable.get()
    breakpoint()
