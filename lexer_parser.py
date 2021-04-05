"""
Roberta González Garza
A01570010

Mariano García Alipi
A00822247

05/abr/2021

Diseño de compiladores
Avance 1: Análisis de léxico y sintaxis
"""

from ply import lex
from ply import yacc
import sys

# LEXICON

# List of reserved words.
reserved = {
    'program':      'PROGRAM_KEYWORD',
    'main':         'MAIN_KEYWORD',
    'class':        'CLASS_KEYWORD',
    'inherits':     'INHERITS',
    'attributes':   'ATTRIBUTES_KEYWORD',
    'variables':    'VARS_KEYWORD',
    'byevar':       'END_VARS', # temp
    'methods':      'METHODS_KEYWORD',
    'function':     'FUNCTION',
    'return':       'RETURN',
    'read':         'READ',
    'write':        'WRITE',
    'int':          'INT',
    'float':        'FLOAT',
    'char':         'CHAR',
    'void':         'VOID',
    'if':           'IF',
    'elsif':        'ELSIF',
    'else':         'ELSE',
    'while':        'WHILE',
    'do':           'DO',
    'from':         'FROM',
    'to':           'TO'
}

# List of token names.
tokens = [
    'COMMA',
    'PERIOD',
    'COLON',
    'SEMICOLON',
    'LEFT_PARENTHESIS',
    'RIGHT_PARENTHESIS',
    'LEFT_CURLY',
    'RIGHT_CURLY',
    'LEFT_BRACKET',
    'RIGHT_BRACKET',
    'NOT_EQUALS',
    'EQUALS_COMPARISON',
    'EQUALS_ASSIGNMENT',
    'LESS_THAN',
    'GREATER_THAN',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'AND',
    'OR',
    'ID',
    'CONST_INT',
    'CONST_FLOAT',
    'CONST_STRING'
] + list(reserved.values())

# Regular expression rules for simple tokens.
t_COMMA         = r','
t_PERIOD        = r'\.'
t_COLON         = r':'
t_SEMICOLON     = r';'
t_LEFT_PARENTHESIS  = r'\('
t_RIGHT_PARENTHESIS = r'\)'
t_LEFT_CURLY        = r'\{'
t_RIGHT_CURLY       = r'\}'
t_LEFT_BRACKET      = r'\['
t_RIGHT_BRACKET     = r'\]'
t_NOT_EQUALS        = r'!='
t_EQUALS_COMPARISON = r'=='
t_EQUALS_ASSIGNMENT = r'='
t_LESS_THAN     = r'<'
t_GREATER_THAN  = r'>'
t_PLUS          = r'\+'
t_MINUS         = r'\-'
t_MULTIPLY      = r'\*'
t_DIVIDE        = r'\/'
t_AND           = r'&&'
t_OR            = r'\|\|'
t_ignore        = r' '

# More complex regular expression rules.
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    # The second argument ('ID') is a default value
    # in case t.value is not in 'reserved'.
    t.type = reserved.get(t.value, 'ID')
    return t

def t_CONST_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CONST_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CONST_STRING(t):
    # String delimiters are "".
    # Allow everything but new line characters.
    # Allow " by escaping it with \.
    r'\"([^\\\n]|(\\.))+\"'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    pass

def t_error(t):
    print(f'Unexpected character at line {t.lineno}: {t.value}')
    t.lexer.skip(1)
    pass

###############################################################################
# GRAMMAR

# The parser grammar rules.
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE')
)

def p_program(p):
    '''
    program : PROGRAM_KEYWORD ID SEMICOLON classes vars funcs main
    '''
    p[0] = tuple(p[1:])

def p_classes(p):
    '''
    classes : CLASS_KEYWORD ID inheritance LEFT_CURLY attributes methods RIGHT_CURLY SEMICOLON classes
            | empty
    '''
    p[0] = tuple(p[1:])

def p_inheritance(p):
    '''
    inheritance : INHERITS ID
                | empty
    '''
    p[0] = tuple(p[1:])

def p_attributes(p):
    '''
    attributes : ATTRIBUTES_KEYWORD vars_1
               | empty
    '''
    p[0] = tuple(p[1:])

def p_methods(p):
    '''
    methods : METHODS_KEYWORD funcs
            | empty
    '''
    p[0] = tuple(p[1:])

def p_vars(p):
    '''
    vars : VARS_KEYWORD vars_1 END_VARS
         | empty
    '''
    p[0] = tuple(p[1:])

def p_vars_1(p):
    '''
    vars_1 : var_type COLON vars_2 vars_arr SEMICOLON vars_1
           | var_type COLON vars_2 vars_arr SEMICOLON
    '''
    p[0] = tuple(p[1:])

def p_vars_arr(p):
    '''
    vars_arr : LEFT_BRACKET CONST_INT RIGHT_BRACKET
             | LEFT_BRACKET variable RIGHT_BRACKET
             | empty
    '''
    p[0] = tuple(p[1:])

def p_type(p):
    '''
    type : INT
         | FLOAT
         | CHAR
    '''
    p[0] = p[1]

def p_var_type(p):
    '''
    var_type : type
             | ID
    '''
    p[0] = p[1]

def p_vars_2(p):
    '''
    vars_2 : ID COMMA vars_2
           | ID
    '''
    p[0] = tuple(p[1:])

def p_funcs(p):
    '''
    funcs : FUNCTION func_type ID LEFT_PARENTHESIS parameters RIGHT_PARENTHESIS LEFT_CURLY vars block_1 RIGHT_CURLY SEMICOLON funcs_1
    '''
    p[0] = tuple(p[1:])

def p_funcs_1(p):
    '''
    funcs_1 : funcs
            | empty
    '''
    p[0] = tuple(p[1:])

def p_func_type(p):
    '''
    func_type : type
              | VOID
    '''
    p[0] = p[1]

def p_parameters(p):
    '''
    parameters : parameters_1
               | empty
    '''
    p[0] = tuple(p[1:])

def p_parameters_1(p):
    '''
    parameters_1 : var_type COLON ID parameters_2
    '''
    p[0] = tuple(p[1:])

def p_parameters_2(p):
    '''
    parameters_2 : COMMA parameters_1
                 | empty
    '''
    p[0] = tuple(p[1:])

def p_main(p):
    '''
    main : MAIN_KEYWORD LEFT_PARENTHESIS RIGHT_PARENTHESIS block SEMICOLON
    '''
    p[0] = tuple(p[1:])

def p_block(p):
    '''
    block : LEFT_CURLY block_1 RIGHT_CURLY
    '''
    p[0] = tuple(p[1:])

def p_block_1(p):
    '''
    block_1 : statement block_1
            | empty
    '''
    p[0] = tuple(p[1:])

def p_statement(p):
    '''
    statement : statement_1 SEMICOLON
    '''
    p[0] = tuple(p[1:])

def p_statement_1(p):
    '''
    statement_1 : assignment
                | func_call
                | return
                | read
                | write
                | decision
                | cond_loop
                | non_cond_loop
                | empty
    '''
    p[0] = tuple(p[1:])

def p_assignment(p):
    '''
    assignment : variable EQUALS_ASSIGNMENT expression
               | variable EQUALS_ASSIGNMENT func_call
    '''
    p[0] = tuple(p[1:])

def p_variable(p):
    '''
    variable : ID LEFT_BRACKET exp COMMA exp RIGHT_BRACKET
             | ID PERIOD ID
             | ID
    '''
    p[0] = tuple(p[1:])

def p_expression(p):
    '''
    expression : exp relational_operator exp
               | exp
    '''
    p[0] = tuple(p[1:])

def p_relational_operator(p):
    '''
    relational_operator : NOT_EQUALS
                        | EQUALS_COMPARISON
                        | LESS_THAN
                        | GREATER_THAN
                        | AND
                        | OR
    '''
    p[0] = p[1]

def p_exp(p):
    '''
    exp : term PLUS exp
        | term MINUS exp
        | term
    '''
    p[0] = tuple(p[1:])

def p_term(p):
    '''
    term : factor MULTIPLY factor
         | factor DIVIDE factor
         | factor
    '''
    p[0] = tuple(p[1:])

def p_factor(p):
    '''
    factor : LEFT_PARENTHESIS expression RIGHT_PARENTHESIS
           | constant
           | variable
           | func_call
           | PLUS constant
           | MINUS constant 
    '''
    p[0] = tuple(p[1:])

def p_constant(p):
    '''
    constant : CONST_INT
             | CONST_FLOAT
    '''
    p[0] = p[1]

def p_func_call(p):
    '''
    func_call : ID PERIOD ID LEFT_PARENTHESIS func_call_1 RIGHT_PARENTHESIS
              | ID LEFT_PARENTHESIS func_call_1 RIGHT_PARENTHESIS
    '''
    p[0] = tuple(p[1:])

def p_func_call_1(p):
    '''
    func_call_1 : func_call_2
                | empty
    '''
    p[0] = tuple(p[1:])

def p_func_call_2(p):
    '''
    func_call_2 : variable func_call_3
                | exp func_call_3
    '''
    p[0] = tuple(p[1:])

def p_func_call_3(p):
    '''
    func_call_3 : COMMA func_call_2
                | empty
    '''
    p[0] = tuple(p[1:])

def p_return(p):
    '''
    return : RETURN LEFT_PARENTHESIS exp RIGHT_PARENTHESIS
    '''
    p[0] = tuple(p[1:])

def p_read(p):
    '''
    read : READ LEFT_PARENTHESIS read_1 RIGHT_PARENTHESIS
    '''
    p[0] = tuple(p[1:])

def p_read_1(p):
    '''
    read_1 : variable read_2
    '''
    p[0] = tuple(p[1:])

def p_read_2(p):
    '''
    read_2 : COMMA variable read_2
           | empty
    '''
    p[0] = tuple(p[1:])

def p_write(p):
    '''
    write : WRITE LEFT_PARENTHESIS write_1 RIGHT_PARENTHESIS
    '''
    p[0] = tuple(p[1:])

def p_write_1(p):
    '''
    write_1 : expression write_2
            | CONST_STRING write_2
    '''
    p[0] = tuple(p[1:])

def p_write_2(p):
    '''
    write_2 : COMMA write_1
            | empty
    '''
    p[0] = tuple(p[1:])

def p_decision(p):
    '''
    decision : IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS block elsif else
    '''
    p[0] = tuple(p[1:])

def p_elsif(p):
    '''
    elsif : ELSIF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS block elsif
          | empty
    '''
    p[0] = tuple(p[1:])

def p_else(p):
    '''
    else : ELSE block
         | empty
    '''
    p[0] = tuple(p[1:])

def p_cond_loop(p):
    '''
    cond_loop : WHILE LEFT_PARENTHESIS expression RIGHT_PARENTHESIS DO block
    '''
    p[0] = tuple(p[1:])

def p_non_cond_loop(p):
    '''
    non_cond_loop : FROM ID EQUALS_ASSIGNMENT exp TO exp DO block
    '''
    p[0] = tuple(p[1:])

def p_empty(p):
    '''
    empty : 
    '''
    return None

class SyntaxError(Exception):
    pass

def p_error(p):
    if p == None:
        token = 'End of file'
    else:
        token = f'{p.type}(\'{p.value}\') at line {p.lineno}'
    raise SyntaxError(token)

###############################################################################
    
# Open a text file
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
    filename = input('Path to file: ')

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

# Build the lexer.
lexer = lex.lex()
lexer.input(lines)

# Build the parser.
parser = yacc.yacc()
try:
    print('Parsing...')
    parser.parse(lines, debug=debug_mode)
    print('Correct syntax.')
except SyntaxError as e:
    print(f'Syntax error: unexpected {e.args[0]}')

print()