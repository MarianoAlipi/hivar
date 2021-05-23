# FuncDirectory is a directions table for functions, it includes the function id, the position for the quad where it starts, and the return var

FuncDirectory = {}
func_prefix = ''


# dict with
# key: func_id
# val:
#   dir -> quad index
#   return -> endfunc quad
#   return_var -> id to return
#   params -> list of str tuples(id, type)
#   local_vars -> st of str tuples(id, type)

# INTERNAL METHODS

def add_prefix(func_id):
    # manages func prefix for functions inside classes, empty if global scope
    #  Persona.   +    func_id
    return func_prefix + func_id


def validate_existing(func_id):
    if func_id not in FuncDirectory:
        raise Exception(
            f'Function "{func_id}" not in funcdirectory')
    return add_prefix(func_id)


def validate_new(func_id):
    if func_id in FuncDirectory:
        raise Exception(
            f'Function "{func_id}" already in funcdirectory')
    return add_prefix(func_id)

# USED FOR DEBUGGING ONLY


def get():
    return FuncDirectory


# EXTERNAL METHODS
def set_return_quad(func_id, returning_quad):
    func_id = validate_existing(func_id)
    FuncDirectory[func_id]['return'] = returning_quad


def set_return_quad_val(func_id, return_to):
    # se llama despues del = de una func call y settea el valor del return quad a 1+ el counter
    func_id = validate_existing(func_id)
    FuncDirectory[func_id]['return'].set_res(return_to)


def set_return_var_id(func_id, return_var_id):
    func_id = validate_existing(func_id)
    FuncDirectory[func_id]['return_var'] = return_var_id


def get_return_var_id(func_id):
    func_id = validate_existing(func_id)
    return FuncDirectory[func_id]['return_var']


def save_func_to_directory(func_id, starting_quad_position):
    func_id = validate_new(func_id)
    FuncDirectory[func_id] = {
        'dir': starting_quad_position, 'return': None, 'return_var': None, 'params': None, 'local_vars': None}


def set_starting_quad_to_func(func_id, starting_quad_position):
    func_id = validate_existing(func_id)
    FuncDirectory[func_id]['dir'] = starting_quad_position


def get_func_from_directory(func_id):
    func_id = validate_existing(func_id)
    return FuncDirectory[func_id]['dir']


def update_func_prefix(new_prefix):
    func_prefix = new_prefix


def save_params_to_directory(st):
    # rn im saving jsut the params, in the future we can use these to calculate how much space will be needed
    func_id = st.current_scope_name()
    func_obj = st.current_scope().get_func_from_id(func_id)
    params = func_obj.params()

    # will be useful if we save size
    #total_size = 0
    #var_objects = st.current_scope().vars()
    # for param in params:
    #    if param[1] in var_objects:
    #        total_size += var_objects[param[1]].get_size()

    func_id = validate_existing(func_id)
    FuncDirectory[func_id]['params'] = params


def save_local_vars_to_directory(st):
    # rn im saving just the local_vars, in the future we can use these to calculate how much space will be needed
    local_vars = st.current_scope().vars()
    func_id = st.current_scope_name()
    func_id = validate_existing(func_id)
    formatted_vars = []
    for key in local_vars:
        formatted_vars.append(
            (local_vars[key].name(), local_vars[key].var_type()))

    # will be useful if we save size
    #total_size = 0
    #var_objects = st.current_scope().vars()
    # for formatted_var in formatted_vars:
    #    if formatted_var[0] in var_objects:
    #        total_size += var_objects[formatted_var[0]].get_size()

    FuncDirectory[func_id]['local_vars'] = formatted_vars


def save_temp_var_to_directory(st, var_name, var_type):
    func_id = st.current_scope_name()
    func_id = validate_existing(func_id)
    FuncDirectory[func_id]['local_vars'].append((var_name, var_type))


def get_local_vars_from_id(func_id):
    func_id = validate_existing(func_id)
    return FuncDirectory[func_id]['local_vars']
