"""
Roberta González Garza
A01570010

Mariano García Alipi
A00822247
"""

from ply import lex
from ply import yacc
from structures.symbol_table import SymbolTable, Variable
from utils.semantics import match_operators
from structures.quadruples import Quad
from reserved import reserved, tokens


# Regular expression rules for simple tokens.
t_COMMA = r','
t_PERIOD = r'\.'
t_COLON = r':'
t_SEMICOLON = r';'
t_LEFT_PARENTHESIS = r'\('
t_RIGHT_PARENTHESIS = r'\)'
t_LEFT_CURLY = r'\{'
t_RIGHT_CURLY = r'\}'
t_LEFT_BRACKET = r'\['
t_RIGHT_BRACKET = r'\]'
t_NOT_EQUALS = r'!='
t_EQUALS_COMPARISON = r'=='
t_LESS_EQUALS = r'<='
t_GREATER_EQUALS = r'>='
t_LESS_THAN = r'<'
t_GREATER_THAN = r'>'
t_EQUALS_ASSIGNMENT = r'='
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_AND = r'&&'
t_OR = r'\|\|'
t_ignore = r' '


# Regular expression rules for complex tokens.
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

#############
## GRAMMAR ##
#############


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
    classes : CLASS_KEYWORD ID save_class push_scope inheritance LEFT_CURLY attributes methods RIGHT_CURLY pop_scope SEMICOLON classes
            | empty
    '''
    p[0] = tuple(p[1:])


def p_save_class(p):
    '''
    save_class :
    '''
    st = SymbolTable.get()
    st.set_curr_id(p[-1])
    st.add_class(p[-1])


def p_inheritance(p):
    '''
    inheritance : INHERITS ID
                | empty
    '''
    p[0] = tuple(p[1:])


def p_attributes(p):
    '''
    attributes : ATTRIBUTES_KEYWORD vars_1 set_vars_as_attrs
               | empty
    '''
    p[0] = tuple(p[1:])


def p_set_vars_as_attrs(p):
    '''
    set_vars_as_attrs :
    '''
    st = SymbolTable.get()
    st.current_scope().set_vars_as_attrs()


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
    vars_1 : var_type COLON vars_2 vars_arr save_var SEMICOLON vars_1
           | var_type COLON vars_2 vars_arr save_var SEMICOLON
    '''
    p[0] = tuple(p[1:])


def p_vars_arr(p):
    '''
    vars_arr : LEFT_BRACKET vars_arr_1 RIGHT_BRACKET
             | empty
    '''
    p[0] = tuple(p[1:])


def p_vars_arr_1(p):
    '''
    vars_arr_1 : vars_arr_2 COMMA vars_arr_2
               | vars_arr_2
    '''
    p[0] = tuple(p[1:])


def p_vars_arr_2(p):
    '''
    vars_arr_2 : CONST_INT
               | exp
    '''
    p[0] = tuple(p[1:]) if len(p[1:]) > 1 else p[1]


def p_type(p):
    '''
    type : INT save_type
         | FLOAT save_type
         | CHAR save_type
    '''
    p[0] = p[1]


def p_var_type(p):
    '''
    var_type : type
             | ID save_type
    '''
    p[0] = p[1]


def p_vars_2(p):
    '''
    vars_2 : ID save_id save_var COMMA vars_2
           | ID save_id
    '''
    p[0] = tuple(p[1:])


def p_funcs(p):
    '''
    funcs : FUNCTION func_type ID save_id save_func push_scope LEFT_PARENTHESIS parameters RIGHT_PARENTHESIS LEFT_CURLY vars block_1 RIGHT_CURLY pop_scope SEMICOLON funcs_1
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
              | VOID save_type
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
    parameters_1 : var_type save_type COLON ID save_id save_parameter parameters_2
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
    assignment : variable EQUALS_ASSIGNMENT exp
               | variable EQUALS_ASSIGNMENT func_call
    '''
    p[0] = tuple(p[1:])
    # TODO assignment


def p_variable(p):
    '''
    variable : ID LEFT_BRACKET exp COMMA exp RIGHT_BRACKET
             | ID PERIOD ID
             | ID set_var_as_curr
    '''
    p[0] = tuple(p[1:])


def p_set_var_as_curr(p):
    '''
    set_var_as_curr :
    '''
    st = SymbolTable.get()
    # start always by setting to none, the logic will check if these exists and act accordingly
    curr_var = st.current_scope().get_var_from_id(p[-1])
    st.set_curr_id(p[-1])
    st.set_curr_type(curr_var.var_type())


def p_expression(p):
    '''
    expression : exp relational_op exp
               | exp
    '''
    p[0] = tuple(p[1:])


def p_relational_op(p):
    '''
    relational_op : NOT_EQUALS
                  | EQUALS_COMPARISON
                  | LESS_EQUALS
                  | GREATER_EQUALS
                  | LESS_THAN
                  | GREATER_THAN
                  | AND
                  | OR
    '''
    p[0] = p[1]


def p_exp(p):
    '''
    exp : term eval_exp PLUS push_operator exp
        | term eval_exp MINUS push_operator exp
        | term eval_exp
    '''
    p[0] = tuple(p[1:])


def p_eval_exp(p):
    '''
    eval_exp :
    '''
    st = SymbolTable.get()
    if st.operators().top() == '+' or st.operators().top() == '-':
        eval_exp_or_term(st)


def eval_exp_or_term(st):
    # TODO fondos falsos
    # creo que es de if top == ')' exp otravez?

    right_op = st.operands().pop()
    right_type = st.op_types().pop()
    left_op = st.operands().pop()
    left_type = st.op_types().pop()
    operator = st.operators().pop()
    if operator == '(' or operator == ')':
        breakpoint()

    res_type = match_operators(left_type, right_type, operator)
    temp_var_name = f't_{st.t_counter()}'
    print(f'{left_op}.{left_type} {operator} {right_op}.{right_type} = {temp_var_name}.{res_type}')
    st.add_to_counter()
    st.save_temp_var(temp_var_name, res_type)

    quad = Quad(operator, left_op, right_op, temp_var_name)

    st.quads().append(quad)
    st.operands().push(temp_var_name)
    st.op_types().push(res_type)


def p_term(p):
    '''
    term : factor eval_term MULTIPLY push_operator term
         | factor eval_term DIVIDE push_operator term
         | factor eval_term
    '''
    p[0] = tuple(p[1:])


def p_eval_term(p):
    '''
    eval_term :
    '''
    st = SymbolTable.get()
    if st.operators().top() == '*' or st.operators().top() == '/':
        eval_exp_or_term(st)


def p_push_operator(p):
    '''
    push_operator :
    '''
    op = p[-1]
    st = SymbolTable.get()
    st.operators().push(op)


def p_factor(p):
    # TODO add logic after getting fake ceiling
    '''
    factor : LEFT_PARENTHESIS push_operator expression RIGHT_PARENTHESIS push_operator save_operand
           | constant save_operand
           | variable save_operand
           | func_call save_operand
           | PLUS set_constant_sign constant save_operand
           | MINUS set_constant_sign constant save_operand
    '''
    p[0] = tuple(p[1:])


def p_save_operand(p):
    '''
    save_operand :
    '''
    st = SymbolTable.get()
    st.operands().push(st.current_id())
    st.op_types().push(st.current_type())


def p_set_constant_sign(p):
    '''
    set_constant_sign : 
    '''
    st = SymbolTable.get()
    st.curr_constant_sign = p[-1]


def p_constant(p):
    '''
    constant : CONST_INT save_int_var_as_current
             | CONST_FLOAT save_float_var_as_current
    '''
    p[0] = p[1]


def p_save_int_var_as_current(p):
    '''
    save_int_var_as_current : 
    '''
    st = SymbolTable.get()
    st.set_curr_type('int')
    st.set_curr_id(p[-1])

    if st.constant_sign() == '-':
        st.set_curr_id(p[-1] * -1)
    else:
        st.set_curr_id(p[-1])
    st.set_constant_sign('+')


def p_save_float_var_as_current(p):
    '''
    save_float_var_as_current : 
    '''
    st = SymbolTable.get()
    st.set_curr_type('float')
    st.set_curr_id(p[-1])

    if st.constant_sign() == '-':
        st.set_curr_id(p[-1] * -1)
    else:
        st.set_curr_id(p[-1])
    st.set_constant_sign('+')


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
    func_call_2 : exp func_call_3
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


def p_save_type(p):
    '''
    save_type :
    '''
    st = SymbolTable.get()
    st.set_curr_type(p[-1])


def p_save_id(p):
    '''
    save_id :
    '''
    st = SymbolTable.get()
    st.set_curr_id(p[-1])


def p_save_var(p):
    '''
    save_var :
    '''
    st = SymbolTable.get()
    st.save_var()


def p_save_func(p):
    '''
    save_func :
    '''
    st = SymbolTable.get()
    st.save_func()


def p_push_scope(p):
    '''
    push_scope :
    '''
    st = SymbolTable.get()
    st.push_scope()


def p_pop_scope(p):
    '''
    pop_scope :
    '''
    st = SymbolTable.get()
    st.pop_scope()


def p_save_parameter(p):
    '''
    save_parameter :
    '''
    st = SymbolTable.get()
    st.save_parameter()


# Build the lexer and parser.
lexer = lex.lex()
parser = yacc.yacc()
