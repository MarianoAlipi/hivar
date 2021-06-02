from lexer_parser import lexer, parser
from file_manager import get_file_content
from structures.symbol_table import SymbolTable
from structures.virtual_machine import VirtualMachine
DEBUG_MODE = 0

lines = get_file_content("tests/objetos.txt")
lexer.input(lines)

try:
    print('\nParsing...')
    parser.parse(lines, debug=DEBUG_MODE)
    print('Correct syntax.\n')
except SyntaxError as e:
    print(f'Syntax error: unexpected {e.args[0]}')

if DEBUG_MODE:
    st = SymbolTable.get()
    st.print_quads()

try:
    print('starting execution...')
    vm = VirtualMachine.get()
    vm.execute_quads()
    print('Successful execution.')
except Exception as err:
    raise Exception(
        f'Something went wrong during the execution: {err}'
    )
