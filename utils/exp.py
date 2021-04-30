from utils.semantics import match_operators
from structures.quadruples import Quad

def eval_exp_or_term(st):
    right_op = st.operands().pop()
    right_type = st.op_types().pop()
    left_op = st.operands().pop()
    left_type = st.op_types().pop()
    operator = st.operators().pop()

    res_type = match_operators(left_type, right_type, operator)
    temp_var_name = f't_{st.t_counter()}'
    #print(f'{left_op}.{left_type} {operator} {right_op}.{right_type} = {temp_var_name}.{res_type}')
    st.add_to_counter()
    st.save_temp_var(temp_var_name, res_type)

    quad = Quad(operator, left_op, right_op, temp_var_name)

    st.quads().append(quad)
    st.operands().push(temp_var_name)
    st.op_types().push(res_type)

def assign_to_var(st):
    right_op = ''
    left_op = st.operands().pop()
    left_type = st.op_types().pop()
    operator = '='
    res_var = st.var_to_assign()
    res_var_type = st.current_scope().get_var_from_id(res_var).var_type()
    if res_var_type != left_type:
        raise Exception(
            f'Problem while assigning var {res_var} types do not match.left_op: {left_op}, right_op: {right_op}, operator: {operator}. Error: {err}')

    quad = Quad(operator, left_op, right_op, res_var)

    st.quads().append(quad)