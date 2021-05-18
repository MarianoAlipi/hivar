from lexer_parser import lexer, parser
from file_manager import get_file_content
from structures.symbol_table import SymbolTable
from virtual_machine import VirtualMachine

DEBUG_MODE = 0

lines = get_file_content("tests/funcs.txt")
lexer.input(lines)

try:
    print('Parsing...')
    parser.parse(lines, debug=DEBUG_MODE)
    print('Correct syntax.')
except SyntaxError as e:
    print(f'Syntax error: unexpected {e.args[0]}')

# if DEBUG_MODE:
st = SymbolTable.get()
st.print_quads()
breakpoint()

# Virtual machine
vm = VirtualMachine.get()
vm.execute(st)