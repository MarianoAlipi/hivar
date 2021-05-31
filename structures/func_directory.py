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

def prefix(func_id):
    # manages func prefix for functions inside classes, empty if global scope
    #  Persona.   +    func_id
    return func_prefix + func_id


def validate_existing(func_id, continue_execution=False):
    # checks if a function exists, can raise exception or continue execution if specified
    if prefix(func_id) not in FuncDirectory:
        if continue_execution:
            return False
        else:
            raise Exception(
                f'Function "{func_id}" not in funcdirectory')
    return prefix(func_id)


def validate_new(func_id):
    if prefix(func_id) in FuncDirectory:
        raise Exception(
            f'Function "{func_id}" already in funcdirectory')
    return prefix(func_id)


def get():
    # USED FOR DEBUGGING ONLY
    return FuncDirectory


# EXTERNAL METHODS
def set_return_quad(func_id, returning_quad):
    func_id = validate_existing(func_id)
    FuncDirectory[func_id]['return'] = returning_quad


def set_return_quad_val(func_id, return_to):
    # called after the = iin a func_call
    # return_to is the returning quad index + 1 (next quad)
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
    # creates a new function with empty vals as placeholders
    FuncDirectory[func_id] = {
        'dir': starting_quad_position, 'return': None, 'return_var': None, 'params': None, 'local_vars': None}


def set_starting_quad_to_func(func_id, starting_quad_position):
    func_id = validate_existing(func_id)
    FuncDirectory[func_id]['dir'] = starting_quad_position


def get_func_from_directory(func_id):
    # gets the starting quad index
    func_id = validate_existing(func_id)
    return FuncDirectory[func_id]['dir']


def update_func_prefix(new_prefix):
    func_prefix = new_prefix


def get_params_from_func_id(func_id):
    return FuncDirectory[func_id]['params']


def save_params_to_directory(st):
    # gets function object using scope name to get params
    func_id = st.current_scope_name()
    func_obj = st.current_scope().get_func_from_id(func_id)
    params = func_obj.params()

    func_id = validate_existing(func_id)
    FuncDirectory[func_id]['params'] = params


def save_local_vars_to_directory(st):
    # gets all vars fromm current scope and saves them to directory
    local_vars = st.current_scope().vars()
    func_id = st.current_scope_name()
    func_id = validate_existing(func_id)
    formatted_vars = []
    for key in local_vars:
        try:
            if type(local_vars[key]) == dict:  # only object vars are dicts
                # for objects, get the attrs and set each as a var
                attributes = local_vars[key]
                for attr in attributes:
                    formatted_vars.append(
                        (attributes[attr].name(), attributes[attr].var_type()))
            else:
                # for simple vars, jusut add them directly
                formatted_vars.append(
                    (local_vars[key].name(), local_vars[key].var_type()))
        except Exception as err:
            breakpoint()
            print(err)
    FuncDirectory[func_id]['local_vars'] = formatted_vars


def save_temp_var_to_directory(st, var_name, var_type):
    # saves temmp vars as local vars to be used in ERA
    func_id = st.current_scope_name()
    func_id = validate_existing(func_id)
    FuncDirectory[func_id]['local_vars'].append((var_name, var_type))


def get_local_vars_from_id(func_id):
    func_id = validate_existing(func_id)
    return FuncDirectory[func_id]['local_vars']
