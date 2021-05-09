# FuncDirectory is a directions table for functions, it includes the function id, the position for the quad where it starts, and the return var

FuncDirectory = {}
func_prefix = ''


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
        'dir': starting_quad_position, 'return': None, 'return_var': None}


def get_func_from_directory(func_id):
    func_id = validate_existing(func_id)
    return FuncDirectory[func_id]['dir']


def update_func_prefix(new_prefix):
    func_prefix = new_prefix
