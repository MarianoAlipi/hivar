from lexer_parser import lexer, parser, SyntaxError
from file_manager import get_file_content
from structures.symbol_table import SymbolTable
from structures.virtual_machine import VirtualMachine
import sys

DEBUG_MODE = 0

file = ''

print(
'''
The
   #  #  #  #   #   #    ###
   ####  #   # #   ###   ####
   #  #  #    #   #   #  #  #
                   programming language
''')

if len(sys.argv) >= 2:
    file = sys.argv[1]
    if len(sys.argv) >= 3:
        if int(sys.argv[2]) == 1:
            DEBUG_MODE = 1
else:
    file = input('File to run: ')
    print()

lines = get_file_content(file)
lexer.input(lines)

try:
    print('Compiling...')
    parser.parse(lines, debug=DEBUG_MODE)
    print('Compiled successfully.\n')
except SyntaxError as e:
    print(f'Syntax error: unexpected token at line {e.args[1]}: {e.args[0]}.\nMissing semicolon?\n')
    exit(1)
except Exception as e:
    print(f'Error: {e.args[0]}\n')
    exit(1)

if DEBUG_MODE:
    st = SymbolTable.get()
    st.print_quads()

try:
    print('Starting execution...')
    print('---------------------\n')
    vm = VirtualMachine.get()
    vm.execute_quads()
    print('\n---------------------')
    print('Successful execution.')
except Exception as err:
    print('\n---------------------')
    print(f'Oh no! Something went wrong during the execution.')
    print(err)
print()
