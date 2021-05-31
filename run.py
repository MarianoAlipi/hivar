from lexer_parser import lexer, parser
from file_manager import get_file_content
from structures.symbol_table import SymbolTable
from structures.virtual_machine import VirtualMachine
DEBUG_MODE = 1

lines = get_file_content("tests/objetos.txt")
lexer.input(lines)

try:
    print('Parsing...')
    parser.parse(lines, debug=DEBUG_MODE)
    print('Correct syntax.')
except SyntaxError as e:
    print(f'Syntax error: unexpected {e.args[0]}')


st = SymbolTable.get()
st.print_quads()

try:
    vm = VirtualMachine.get()
    vm.execute_quads()
    print('Successful execution.')
except Exception as err:
    raise Exception(
        f'Something went wrong during the execution: {err}'
    )
