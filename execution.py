from structures.memory import Memory, MemoryChunk, print_literal_memory
from structures.func_directory import get_local_vars_from_id, FuncDirectory, get_func_from_directory
from utils.runtime import has_dimensions, get_size, is_cte
from structures.index_handler import matrix_index, array_index


def init_memory(memory, func_id):
    # get local vars and insert each in its memory
    new_vars = get_local_vars_from_id(func_id)
    if func_id == 'global':
        global_mem = memory.get_global_memory()
        for var in new_vars:
            try:
                has_dims = has_dimensions(var[0])
            except Exception:
                # if execution fails, then it has no dims
                has_dims = False

            # inits memory according to if it's an array/matrix, object or simple var
            if has_dims:
                var_size = get_size(var[0])
                global_mem.init_array(var[0], var[1], 'global', var_size)
            else:
                global_mem.init_address(var[0], var[1], 'global')

            # TODOBJ checar si es un objeto, si si la globalmem.init_object

        return global_mem
    else:
        # if execution fails, then it has no dims
        local_mem = MemoryChunk()
        for var in new_vars:
            try:
                has_dims = has_dimensions(var[0])
            except Exception:
                # if execution fails, then it has no dims
                has_dims = False

             # inits memory according to if it's an array/matrix, object or simple var
            if has_dims:
                var_size = get_size(var[0])
                local_mem.init_array(var[0], var[1], 'local', var_size)
            else:
                local_mem.init_address(var[0], var[1], 'local')
        return local_mem


def init_object_func_memory(memory, var_id, method_id):
    # get local vars and insert each in its memory
    new_vars = get_local_vars_from_id(method_id)
    local_mem = MemoryChunk()
    for var in new_vars:
        local_mem.init_address(var[0], var[1], 'local')
    return local_mem


def process_quad(vm, quad):
    op, left, right, res = quad.unpack()
    memory = Memory.get()
    # giant switch statement according to instruction
    if op == '=':
        if is_cte(left):
            memory.active_memory().set_cte_val_for_id(res, left)
        else:
            memory.active_memory().set_val_for_id(res, left)
        vm.point_to_next_quad()
    elif op in ['+', '-', '/', '*', '<', '>', '==', '!=', '<=', '>=', '&&', '||']:
        memory.active_memory().solve_quad(op, res, left, right)
        vm.point_to_next_quad()
    elif op == 'goto':
        vm.set_instruction_pointer(res)
    elif op == 'gotomain':
        vm.set_instruction_pointer(res)
        local_mem = init_memory(memory, 'global')
        memory.locals_memory_stack().push(local_mem)
    elif op == 'gotof':
        comparison_value = memory.active_memory().get_value(left)
        if comparison_value == False:
            vm.set_instruction_pointer(res)
        else:
            vm.point_to_next_quad()
    elif op == 'write':
        if type(res) == str:
            # Print the string removing " and escaping \" and \n
            to_write = res[1:-1]
            i = 0
            while i < len(to_write):
                # If a backslash is found:
                if to_write[i] == '\\':
                    # Escape \"
                    if to_write[i + 1] == '"':
                        to_write = to_write[0:i] + to_write[i + 1:]
                    # Escape \n
                    elif to_write[i + 1] == 'n':
                        to_write = to_write[0:i] + '\n' + to_write[i + 2:]
                    # Escape \\
                    elif to_write[i + 1] == '\\':
                        to_write = to_write[0:i] + '\\' + to_write[i + 2:]
                i += 1
            print(to_write, end='')
        else:
            # Search for the ID's value
            print(memory.active_memory().get_value(res[0]), end='')
        vm.point_to_next_quad()
    elif op == 'read':
        user_input = input('>>> ')
        val = None
        val_type = None
        try:
            val = int(user_input)
            val_type = 'int'
        except ValueError:
            try:
                val = float(user_input)
                val_type = 'float'
            except ValueError:
                val = user_input[0]
                val_type = 'char'
        if len(res) == 1:
            res = res[0]
        elif len(res) == 3:
            res = (res[0], res[2])
        memory.active_memory().set_cte_val_for_id(res, val, val_type)
        vm.point_to_next_quad()
    elif op == 'ERA':
        local_memory = init_memory(memory, res)
        # save new memory on top of tthe execution stack for later
        vm.execution_stack().push(local_memory)
        vm.point_to_next_quad()
    elif op == 'ERAF':
        local_memory = init_object_func_memory(memory, right, res)
        vm.execution_stack().push(local_memory)
        vm.point_to_next_quad()
    elif op == 'gosub':
        # +2 because +1 te points to the quad we're reading now, and another +1 to go to the quad AFTER the func ends
        vm.jump_stack().push(vm.instruction_pointer()+2)
        # gets where to go using function directory
        func_start = get_func_from_directory(res)
        vm.set_instruction_pointer(func_start)
        # assign params and then clear them
        assign_params(vm, memory, res)
        vm.clear_func_params()
        # finally push new memory stack
        memory.locals_memory_stack().push(vm.execution_stack().pop())
    elif op == 'param':
        param_address = memory.active_memory().find_address(left)
        vm.add_func_param(param_address)
        vm.point_to_next_quad()
    elif op == 'return':
        res_address = memory.active_memory().find_address(res)
        res_value = memory.get_value_from_address(res_address)
        # save the return value in the stack because we will eventually erase the memory, so we don't lose it forever
        vm.execution_stack().push(res_value)
        vm.point_to_next_quad()
    elif op == 'gotoendfunc':
        vm.set_instruction_pointer(vm.jump_stack().pop())
        memory.locals_memory_stack().pop()
    elif op == 'endfunc':
        vm.set_instruction_pointer(vm.jump_stack().pop())
        memory.locals_memory_stack().pop()
    elif op == 'ASSGN':
        # special operation for assigning values among scopes
        res_address = memory.active_memory().find_address(left)
        res_value = vm.execution_stack().pop()
        memory.assign_value_to_address(res_value, res_address)
        vm.point_to_next_quad()
    elif op == 'verifya':
        # used to verify array index
        res_value = memory.active_memory().get_value(right)
        if res_value >= res:
            raise Exception(
                f'Out of bounds: {left} has a value of {res_value}, ' +
                f'must be between 0 and {res}')
        array_index().push(right)
        vm.point_to_next_quad()
    elif op == 'verifyr':
        # used to verify matrix row index
        res_value = memory.active_memory().get_value(right)
        if res_value >= res:
            raise Exception(
                f'Out of bounds: {left} has a value of {res_value}, ' +
                f'must be between 0 and {res}')
        matrix_index().push(res_value)
        vm.point_to_next_quad()
    elif op == 'verifyc':
        # used to verify matrix column index
        res_value = memory.active_memory().get_value(right)
        if res_value >= res:
            raise Exception(
                f'Out of bounds: {left} has a value of {res_value}, ' +
                f'must be between 0 and {res}')
        rows = matrix_index().pop()
        matrix_index().push((rows, res_value))
        vm.point_to_next_quad()
    else:
        breakpoint()
        quad.print()
        vm.point_to_next_quad()


def assign_params(vm, memory, func_id):
    # gets a list of the paramms to assign and their types
    params_to_assign = FuncDirectory[func_id]['params']
    # where params are holds the directions values (in order) of the params
    where_params_are = vm.get_func_params()
    for i in range(0, len(params_to_assign)):
        # finds where the addresses are, gets the value that will fill them, and assigns it
        address_to_fill = vm.execution_stack().top(
        ).find_address(params_to_assign[i][1])
        value_to_fill_with = memory.get_value_from_address(where_params_are[i])
        memory.assign_value_to_address(value_to_fill_with, address_to_fill)
