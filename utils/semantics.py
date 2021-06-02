# functions regarding semantics cube
from structures.semantics_cube import get_cube
ERR = 'err'


def match_operators(left_op, right_op, operator):
    # general type matching function, handles errors in type matching or in op logic
    cube = get_cube()
    try:
        res = cube[left_op][right_op][operator]
        if res is ERR:
            raise Exception("Operand types do not match.")
        return res
    except Exception as err:
        raise Exception(
            f'Problem while checking types. The operands probably do not exist.\nLeft operand: {left_op}\nRight operand: {right_op}\nOperator: {operator}\nError: {err}')
