from utils.semantics import match_operators
from structures.quadruples import Quad
from structures.func_directory import get_return_var_id
from structures.func_directory import set_return_var_id
# evals


def eval_exp_or_term(st):
    right_op = st.operands().pop()
    right_type = st.op_types().pop()
    left_op = st.operands().pop()
    left_type = st.op_types().pop()
    operator = st.operators().pop()

    res_type = match_operators(left_type, right_type, operator)
    temp_var_name = get_temp_var_name(st)
    #print(f'{left_op}.{left_type} {operator} {right_op}.{right_type} = {temp_var_name}.{res_type}')
    st.save_temp_var(temp_var_name, res_type)

    quad = Quad(operator, left_op, right_op, temp_var_name)

    st.quads().append(quad)
    st.operands().push(temp_var_name)
    st.op_types().push(res_type)

# assign


def assign_to_var(st):
    right_op = ''
    left_op = st.operands().pop()
    left_type = st.op_types().pop()
    operator = '='
    res_var = st.var_to_assign().pop()
    res_var_type = st.current_scope().get_var_from_id(res_var).var_type()
    if res_var_type != left_type:
        raise Exception(
            f'Problem while assigning var {res_var} types do not match.left_op: {left_op}, right_op: {right_op}, operator: {operator}. Error: {err}')
    quad = Quad(operator, left_op, right_op, res_var)
    st.quads().append(quad)


def assign_func_to_var(st, p):
    res_var = st.var_to_assign().pop()
    res_var_type = st.current_scope().get_var_from_id(res_var).var_type()
    func_return_var = get_return_var_id(p[-1][0])
    func_return_type = st.current_scope().funcs()[p[-1][0]].return_type()
    if res_var_type != func_return_type:
        raise Exception(
            f'Problem while assigning var {res_var} types do not match.res_var: {res_var}, func_return_var: {func_return_var}')
    quad = Quad('=', func_return_var, '', res_var)
    st.quads().append(quad)

#func_calls and params


def create_param_assignment_quads(st):
    func_name = st.current_params().pop(0)
    param_vals = st.current_params()
    function = st.current_scope().get_func_from_id(func_name)
    param_keys = function.params()
    for i in range(len(param_keys)):
        param_quad = Quad('=', param_vals[i], '', param_keys[i])
        st.quads().append(param_quad)
    func_jump = st.pending_jumps().pop()
    st.quads().append(func_jump)


def set_return_val(st):
    function_type = st.current_scope().get_func_from_id(
        st.current_scope_name()).return_type()
    var_type = st.current_scope().get_var_from_id(st.operands().top()).var_type()
    if function_type != var_type:
        raise Exception(
            f'Problem while returning val for function {st.current_scope_name()} types do not match. function_type: {function_type}, var_type: {var_type}')
    set_return_var_id(st.current_scope_name(), st.operands().top())
# utils


def get_temp_var_name(st):
    temp_var_name = f't_{st.t_counter()}'
    st.add_to_t_counter()
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
