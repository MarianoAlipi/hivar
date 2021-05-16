"""
Roberta González Garza
A01570010

Mariano García Alipi
A00822247
"""

from ply import lex
from ply import yacc
from structures.symbol_table import SymbolTable
from utils.exp import *
from utils.non_linear import *
from utils.semantics import match_operators
from structures.quadruples import Quad
from structures.stack import Stack, push_operator, pop_operator
from reserved import reserved, tokens
from structures.func_directory import (save_func_to_directory, get_func_from_directory,
                                       set_return_quad, set_return_quad_val,
                                       set_return_var_id, get_return_var_id, update_func_prefix,
                                       save_params_to_directory, save_local_vars_to_directory)

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
    program : PROGRAM_KEYWORD ID SEMICOLON save_main_quad classes vars funcs assign_main_quad main
    '''
    p[0] = tuple(p[1:])


def p_assign_main_quad(p):
    '''
    assign_main_quad :
    '''
    save_main_quad(SymbolTable.get())


def p_save_main_quad(p):
    '''
    save_main_quad :
    '''
    assign_res_to_main_quad(SymbolTable.get())


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
    methods : METHODS_KEYWORD update_func_prefix funcs reset_func_prefix
            | empty
    '''
    p[0] = tuple(p[1:])


def p_update_func_prefix(p):
    '''
    update_func_prefix :
    '''
    st = SymbolTable.get()
    update_func_prefix(st.current_scope_name() + '.')


def p_reset_func_prefix(p):
    '''
    reset_func_prefix :
    '''
    update_func_prefix('')


def p_vars(p):
    '''
    vars : VARS_KEYWORD vars_1 END_VARS
         | empty
    '''
    p[0] = tuple(p[1:])


def p_vars_1(p):
    '''
    vars_1 : var_type COLON vars_2 save_var vars_arr SEMICOLON vars_1
           | var_type COLON vars_2 save_var vars_arr SEMICOLON
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
    vars_arr_1 : vars_arr_2 save_i COMMA vars_arr_2 save_j
               | vars_arr_2 save_i
    '''
    p[0] = tuple(p[1:])


def p_save_j(p):
    '''
    save_j :
    '''
    st = SymbolTable.get()
    var_id = [*st.current_scope().vars()][-1]
    var_object = st.current_scope().vars()[var_id]
    var_object.set_j(p[-1])


def p_save_i(p):
    '''
    save_i :
    '''
    st = SymbolTable.get()
    var_id = [*st.current_scope().vars()][-1]
    var_object = st.current_scope().vars()[var_id]
    var_object.set_i(p[-1])


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
    funcs : FUNCTION func_type ID save_id save_func push_scope LEFT_PARENTHESIS parameters save_params_to_fd RIGHT_PARENTHESIS LEFT_CURLY vars save_vars_to_fd block_1 set_returning_quad RIGHT_CURLY pop_scope SEMICOLON funcs_1
          | empty
    '''
    p[0] = tuple(p[1:])


def p_save_vars_to_fd(p):
    '''
    save_vars_to_fd :
    '''
    save_local_vars_to_directory(SymbolTable.get())


def p_save_params_to_fd(p):
    '''
    save_params_to_fd :
    '''
    save_params_to_directory(SymbolTable.get())


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
    assignment : variable set_var_to_assign EQUALS_ASSIGNMENT exp assign_to_var
               | variable set_var_to_assign EQUALS_ASSIGNMENT func_call assign_func_to_var
    '''
    p[0] = tuple(p[1:])


def p_assign_func_to_var(p):
    '''
    assign_func_to_var :
    '''
    assign_func_to_var(SymbolTable.get(), p)


def p_assign_to_var(p):
    '''
    assign_to_var :
    '''
    assign_to_var(SymbolTable.get())


def p_set_var_to_assign(p):
    '''
    set_var_to_assign :
    '''
    st = SymbolTable.get()
    if type(p[-1]) == tuple:
        st.var_to_assign().push(p[-1][0])
    else:
        st.var_to_assign().push(p[-1])


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
    expression : exp relational_op push_operator exp eval_relop
               | exp
    '''
    p[0] = tuple(p[1:])


def p_eval_relop(p):
    '''
    eval_relop :
    '''
    st = SymbolTable.get()
    relops = ['>', '<', '>=', '<=', '==']
    if st.operators().top() in relops:
        eval_exp_or_term(st)


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
    st = SymbolTable.get()
    push_operator(st, p[-1])


def p_pop_operator(p):
    '''
    pop_operator :
    '''
    st = SymbolTable.get()
    pop_operator(st, p[-1])


def p_factor(p):
    '''
    factor : LEFT_PARENTHESIS push_operator expression RIGHT_PARENTHESIS pop_operator save_operand
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
              | ID set_return_quad_val LEFT_PARENTHESIS func_call_1 RIGHT_PARENTHESIS
    '''
    p[0] = tuple(p[1:])
    # TODO cuando sean objetos algo tendremos que hacer con el func_prefix


def p_set_return_quad_val(p):
    '''
    set_return_quad_val :
    '''
    st = SymbolTable.get()
    func_jump = Quad('gosub', None, None, get_func_from_directory(p[-1]))
    st.pending_jumps().push(func_jump)
    # clear params
    st.reset_current_params()
    st.current_params().append(p[-1])


def p_func_call_1(p):
    '''
    func_call_1 : func_call_2 assign_params
                | empty
    '''
    p[0] = tuple(p[1:])


def p_assign_params(p):
    '''
    assign_params :
    '''
    create_param_assignment_quads(SymbolTable.get())


def p_func_call_2(p):
    '''
    func_call_2 : exp save_param func_call_3
    '''
    p[0] = tuple(p[1:])


def p_save_param(p):
    '''
    save_param :
    '''
    st = SymbolTable.get()
    st.current_params().append(flatten(p[-1])[-1])


def p_func_call_3(p):
    '''
    func_call_3 : COMMA func_call_2
                | empty
    '''
    p[0] = tuple(p[1:])


def p_return(p):
    '''
    return : RETURN LEFT_PARENTHESIS exp set_return_val RIGHT_PARENTHESIS
    '''
    p[0] = tuple(p[1:])


def p_set_return_val(p):
    '''
    set_return_val :
    '''
    set_return_val(SymbolTable.get())


def p_set_returning_quad(p):
    '''
    set_returning_quad :
    '''
    st = SymbolTable.get()
    returning_quad = Quad('endfunc', '', '', '')
    st.quads().append(returning_quad)
    set_return_quad(st.current_scope_name(), returning_quad)


def p_read(p):
    '''
    read : READ LEFT_PARENTHESIS read_1 RIGHT_PARENTHESIS
    '''
    p[0] = tuple(p[1:])


def p_read_1(p):
    '''
    read_1 : variable read_expression read_2
    '''
    p[0] = tuple(p[1:])


def p_read_expression(p):
    '''
    read_expression :
    '''
    st = SymbolTable.get()
    quad = Quad('read', '', '', p[-1])
    st.quads().append(quad)


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
    write_1 : expression write_expression write_2
            | CONST_STRING write_expression write_2
    '''
    p[0] = tuple(p[1:])


def p_write_expression(p):
    '''
    write_expression :
    '''
    to_write = flatten(p[-1])
    st = SymbolTable.get()
    quad = Quad('write', '', '', to_write)
    st.quads().append(quad)


def p_write_2(p):
    '''
    write_2 : COMMA write_1
            | empty
    '''
    p[0] = tuple(p[1:])


def p_decision(p):
    '''
    decision : IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS create_gotof create_if_escape block elsif else decision_end
    '''
    p[0] = tuple(p[1:])


def p_elsif(p):
    '''
    elsif : create_goto ELSIF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS create_gotof block elsif
          | empty
    '''
    p[0] = tuple(p[1:])


def p_else(p):
    '''
    else : create_goto ELSE block
         | empty
    '''
    p[0] = tuple(p[1:])


def p_create_if_escape(p):
    '''
    create_if_escape :
    '''
    create_if_escape(SymbolTable.get())


def p_create_gotof(param):
    '''
    create_gotof :
    '''
    create_gotof(SymbolTable.get())


def p_create_goto(param):
    '''
    create_goto :
    '''
    create_goto(SymbolTable.get())


def p_decision_end(param):
    '''
    decision_end :
    '''
    decision_end(SymbolTable.get())


def p_cond_loop(p):
    '''
    cond_loop : WHILE push_while LEFT_PARENTHESIS expression RIGHT_PARENTHESIS eval_while_exp DO block fill_gotof_while
    '''
    p[0] = tuple(p[1:])


def p_fill_gotof_while(p):
    '''
    fill_gotof_while :
    '''
    fill_gotof_while(SymbolTable.get())


def p_eval_while_exp(p):
    '''
    eval_while_exp :
    '''
    eval_while_exp(SymbolTable.get())


def p_push_while(p):
    '''
    push_while :
    '''
    push_while(SymbolTable.get())


def p_non_cond_loop(p):
    '''
    non_cond_loop : FROM ID push_for_id EQUALS_ASSIGNMENT exp save_for_assgn_quad TO exp save_for_cond_quad DO block restart_loop
    '''
    p[0] = tuple(p[1:])


def p_restart_loop(p):
    '''
    restart_loop :
    '''
    restart_loop(SymbolTable.get())


def p_save_for_cond_quad(p):
    '''
    save_for_cond_quad :
    '''
    save_cond_for_quad(SymbolTable.get())


def p_save_for_assgn_quad(p):
    '''
    save_for_assgn_quad :
    '''
    save_for_assgn_quad(SymbolTable.get())


def p_push_for_id(p):
    '''
    push_for_id :
    '''
    st = SymbolTable.get()
    st.for_ids().push(p[-1])


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
        token = f'{p.type}(\'{p.value}\')'
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
    save_func_to_directory(st.current_id(), len(st.quads())+1)


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
