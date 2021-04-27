from structures.symbol_table import Variable
from structures.match_operators import get_cube

ERR = 'err'


def match_operators(left_op, right_op, operator):
    cube = get_cube()
    try:
        res = cube[left_op][right_op][operator]
        if res is ERR:
            raise Exception("operator types did not match")
        return res
    except Exception as err:
        breakpoint()
        raise Exception(
            'Problem while checking types, the operands probably do not exist. '
            f'left_op: {left_op}, right_op: {right_op}, operator: {operator}. Error: {err}')


def solve_quad(quad):
    left_op = quad.left_op()
    right_op = quad.right_op()

    if type(left_op) == Variable:
        left_op = left_op.value()
    if type(right_op) == Variable:
        left_op = left_op.value()

    if quad.operator() == '-':
        quad.set_res(left_op - right_op)
    elif quad.operator() == '+':
        quad.set_res(left_op + right_op)
    elif quad.operator() == '/':
        quad.set_res(left_op / right_op)
    elif quad.operator() == '*':
        quad.set_res(left_op * right_op)
    else:
        raise Exception(
            f'uy no se que paso op {quad.operator()}, left_op {left_op}, right_op {right_op}')

    return quad
