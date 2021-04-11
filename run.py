import sys

from lexer_parser import lexer, parser


file = None
filename = ''
debug_mode = 0
if len(sys.argv) > 1 and sys.argv[1] != None:
    filename = sys.argv[1]

    try:
        if sys.argv[2] != None:
            num = int(sys.argv[2])
    except Exception:
        num = 0
    debug_mode = num if num == 0 or num == 1 else 0

else:
    filename = "tests/input.txt"

try:
    file = open(filename, 'r')
except FileNotFoundError:
    print('File does not exist')
    exit(1)
except Exception:
    print('Unable to open file')
    exit(1)

print()
print('Reading file...')
lines = file.read()
file.close()


lexer.input(lines)

try:
    print('Parsing...')
    parser.parse(lines, debug=debug_mode)
    print('Correct syntax.')
except SyntaxError as e:
    print(f'Syntax error: unexpected {e.args[0]}')


print()
