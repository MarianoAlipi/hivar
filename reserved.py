# List of reserved words.

reserved = {
    'program':      'PROGRAM_KEYWORD',
    'main':         'MAIN_KEYWORD',
    'class':        'CLASS_KEYWORD',
    'attributes':   'ATTRIBUTES_KEYWORD',
    'hivar':        'VARS_KEYWORD',
    'byevar':       'END_VARS',
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
    'LESS_EQUALS',
    'GREATER_EQUALS',
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
