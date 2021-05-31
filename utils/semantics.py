# functions regarding semantics cube
from structures.semantics_cube import get_cube
ERR = 'err'


def match_operators(left_op, right_op, operator):
    # general type matching function, handles errors in type matching or in op logic
    cube = get_cube()
    try:
        res = cube[left_op][right_op][operator]
        if res is ERR:
            raise Exception("operator types did not match")
        return res
    except Exception as err:
        raise Exception(
            'Problem while checking types, the operands probably do not exist. '
            f'left_op: {left_op}, right_op: {right_op}, operator: {operator}. Error: {err}')
