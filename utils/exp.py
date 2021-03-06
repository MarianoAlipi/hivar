from utils.semantics import match_operators
from structures.quadruples import Quad
from structures.func_directory import (get_return_var_id, set_return_var_id,
                                       save_temp_var_to_directory, get_params_from_func_id)

###
# functions used for evaluations
###


def eval_exp_or_term(st):
    # creates operation quad
    # gets operands and operators, matches types, creates temp var and quad
    right_op = st.operands().pop()
    right_type = st.op_types().pop()
    left_op = st.operands().pop()
    left_type = st.op_types().pop()
    operator = st.operators().pop()
    res_type = match_operators(left_type, right_type, operator)
    temp_var_name = get_temp_var_name(st, res_type)
    st.save_temp_var(temp_var_name, res_type)

    quad = Quad(operator, left_op, right_op, temp_var_name)

    st.quads().append(quad)
    st.operands().push(temp_var_name)
    st.op_types().push(res_type)

###
# functions used for assignment statement
###


def assign_to_var(st):
    # creates assignation quad for simple vars and type matches
    right_op = ''
    left_op = st.operands().pop()
    left_type = st.op_types().pop()
    operator = '='
    res_var = st.var_to_assign().pop()
    res_var_type = st.current_scope().get_var_from_id(res_var).var_type()
    if res_var_type != left_type:
        raise Exception(
            f'Problem while assigning variable {res_var}: types do not match.\nLeft operator: {left_op}\nType of the variable to assign: {res_var_type}')
    quad = Quad(operator, left_op, right_op, res_var)
    st.quads().append(quad)


def assign_func_to_var(st, params):
    # creates assignation quad for when assignment is a func call
    res_var = st.var_to_assign().pop()
    res_var_type = st.current_scope().get_var_from_id(res_var).var_type()
    func_id = params[-1][0]
    if func_id == '!':  # this happens when it's a call to a method
        # 4 because 1 is !, 2 is obj_id, 3 is . and 4 is method_id
        func_id = params[-1][4]
    func_return_type = st.current_scope().get_func_from_id(func_id).return_type()
    if res_var_type != func_return_type:
        raise Exception(
            f'Problem while assigning variable {res_var}: types do not match.\nVariable to assign: {res_var}\nFunction: {func_id}\nFunction return type: {func_return_type}')
    quad = Quad('ASSGN', res_var, '', func_id)
    st.quads().append(quad)

###
# functions used for fun_calls and param handling
###


def create_param_assignment_quads(st):
    func_name = st.current_params().pop(0)
    param_vals = st.current_params()
    function = st.current_scope().get_func_from_id(func_name)
    param_keys = []
    full_params = function.params()
    for full_param in full_params:
        param_keys.append(full_param[1])
    # for each param, creates a param quad with the value and id (type matches)
    for i in range(len(param_keys)):
        left_type = st.current_scope().get_var_from_id(
            param_vals[i]).var_type()
        right_params = get_params_from_func_id(func_name)
        right_type = None
        for param in right_params:
            if param[1] == param_keys[i]:
                right_type = param[0]
        if left_type != right_type:
            raise Exception(
                f'Type mismatch: expected \'{right_type}\' parameter but received \'{left_type}\'.'
            )
        param_quad = Quad('param', param_vals[i], '', param_keys[i])
        st.quads().append(param_quad)


def assign_gosub_jump(st):
    # last thing done after a func call, it sets the function jump
    func_jump = st.pending_jumps().pop()
    st.quads().append(func_jump)


def set_return_val(st):
    # type matching
    function_type = st.current_scope().get_func_from_id(
        st.current_scope_name()).return_type()
    var_type = st.current_scope().get_var_from_id(st.operands().top()).var_type()
    if function_type != var_type:
        raise Exception(
            f'Problem while returning value for function \'{st.current_scope_name()}\': types do not match.\nFunction type: {function_type}\nVariable type: {var_type}')
    # creates quad with the value that it must return
    return_quad = Quad('return', '', '', st.operands().top())
    st.quads().append(return_quad)
    set_return_var_id(st.current_scope_name(), st.operands().pop())
    goto_endfunc = Quad('gotoendfunc', '', '', '')
    st.quads().append(goto_endfunc)

###
# utils
###


def get_temp_var_name(st, temp_type):
    temp_var_name = f't_{st.t_counter()}'
    st.add_to_t_counter()
    save_temp_var_to_directory(st, temp_var_name, temp_type)
    return temp_var_name


def flatten(data):
    if isinstance(data, tuple):
        if len(data) == 0:
            return ()
        else:
            return flatten(data[0]) + flatten(data[1:])
    else:
        if data == None:
            return ()
        return (data,)
