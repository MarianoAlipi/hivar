# methods used by the vm in runtime
from structures.symbol_table import SymbolTable


def has_dimensions(var_id):
    # checks if a variable has dimensions and returns them
    st = SymbolTable.get()
    var = st.current_scope().get_var_from_id(var_id)
    if not var.dims():
        return False
    return var.dims()


def get_size(var_id):
    # returns variable size, used during memory allocation
    st = SymbolTable.get()
    var = st.current_scope().get_var_from_id(var_id)
    return var.get_size()


def is_cte(operand):
    # boolean cte
    if operand == 'True' or operand == 'False':
        return True
    # numeric cte
    return type(operand) == int or type(operand) == float
