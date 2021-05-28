from structures.symbol_table import SymbolTable


def has_dimensions(var_id):
    st = SymbolTable.get()
    var = st.current_scope().get_var_from_id(var_id)
    if not var.dims():
        return False
    return var.dims()


def get_size(var_id):
    st = SymbolTable.get()
    var = st.current_scope().get_var_from_id(var_id)
    return var.get_size()
