from structures.memory import Memory, MemoryChunk, print_literal_memory
from structures.func_directory import get_local_vars_from_id, FuncDirectory, get_func_from_directory
from utils.runtime import has_dimensions, get_size
from structures.index_handler import matrix_index, array_index


def is_cte(operand):
    # boolean cte
    if operand == 'True' or operand == 'False':
        return True
    # char cte?
    # numeric cte
    return type(operand) == int or type(operand) == float


def init_memory(memory, func_id):
    new_vars = get_local_vars_from_id(func_id)
    if func_id == 'global':
        global_mem = memory.get_global_memory()
        for var in new_vars:
            try:
                has_dims = has_dimensions(var[0])
            except Exception:
                has_dims = False
            if has_dims:
                var_size = get_size(var[0])
                global_mem.init_array(var[0], var[1], 'global', var_size)
            else:
                global_mem.init_address(var[0], var[1], 'global')
        return global_mem
    else:
        local_mem = MemoryChunk()
        for var in new_vars:
            try:
                has_dims = has_dimensions(var[0])
            except Exception:
                has_dims = False
            if has_dims:
                var_size = get_size(var[0])
                local_mem.init_array(var[0], var[1], 'local', var_size)
            else:
                local_mem.init_address(var[0], var[1], 'local')
        return local_mem


def process_quad(vm, quad):
    op, left, right, res = quad.unpack()
    memory = Memory.get()
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
        memory.active_memory().set_cte_val_for_id(res, user_input)
        vm.point_to_next_quad()
    elif op == 'ERA':
        local_memory = init_memory(memory, res)
        # la guardamos por mientras y está en top por si
        vm.execution_stack().push(local_memory)
        vm.point_to_next_quad()
    elif op == 'gosub':
        # +2 porque +1 te apunta al quad que lees ahorita, y otro +1 después de endfunc quieres ir a sig quad
        vm.jump_stack().push(vm.instruction_pointer()+2)
        func_start = get_func_from_directory(res)
        vm.set_instruction_pointer(func_start)

        assign_params(vm, memory, res)
        vm.clear_func_params()
        memory.locals_memory_stack().push(vm.execution_stack().pop())
    elif op == 'param':
        param_address = memory.active_memory().find_address(left)
        vm.add_func_param(param_address)
        vm.point_to_next_quad()
    elif op == 'return':
        res_address = memory.active_memory().find_address(res)
        res_value = memory.get_value_from_address(res_address)
        vm.execution_stack().push(res_value)
        vm.point_to_next_quad()
    elif op == 'endfunc':
        vm.set_instruction_pointer(vm.jump_stack().pop())
        memory.locals_memory_stack().pop()
    elif op == 'ASSGN':
        res_address = memory.active_memory().find_address(left)
        res_value = vm.execution_stack().pop()
        memory.assign_value_to_address(res_value, res_address)
        vm.point_to_next_quad()
    elif op == 'verifya':
        res_value = memory.active_memory().get_value(right)
        if res_value >= res:
            raise Exception(
                f'Out of bounds: {left} has a value of {res_value}, ' +
                f'must be between 0 and {res}')
        array_index().push(right)
        vm.point_to_next_quad()
    elif op == 'verifyr':
        res_value = memory.active_memory().get_value(right)
        if res_value >= res:
            raise Exception(
                f'Out of bounds: {left} has a value of {res_value}, ' +
                f'must be between 0 and {res}')
        matrix_index().push(res_value)
        vm.point_to_next_quad()
    elif op == 'verifyc':
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
    params_to_assign = FuncDirectory[func_id]['params']
    where_params_are = vm.get_func_params()
    for i in range(0, len(params_to_assign)):
        address_to_fill = vm.execution_stack().top(
        ).find_address(params_to_assign[i][1])
        value_to_fill_with = memory.get_value_from_address(where_params_are[i])
        memory.assign_value_to_address(value_to_fill_with, address_to_fill)
