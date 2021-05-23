from structures.memory import Memory, MemoryChunk, print_literal_memory
from structures.func_directory import get_local_vars_from_id, FuncDirectory, get_func_from_directory


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
            global_mem.init_address(var[0], var[1], 'global')
    else:
        local_mem = MemoryChunk()
        for var in new_vars:
            local_mem.init_address(var[0], var[1], 'local')
        memory.locals_memory_stack().push(local_mem)


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
        init_memory(memory, 'global')
    elif op == 'gotof':
        comparison_value = memory.active_memory().get_value(left)
        if comparison_value == False:
            vm.set_instruction_pointer(res)
        else:
            vm.point_to_next_quad()
    elif op == 'write':
        print(memory.active_memory().get_value(res[0]))
        vm.point_to_next_quad()
    elif op == 'read':
        user_input = input('>>> ')
        memory.active_memory().set_cte_val_for_id(res, user_input)
        vm.point_to_next_quad()
    elif op == 'gosub':
        # +2 porque +1 te apunta al quad que lees ahorita, y otro +1 después de endfunc quieres ir a sig quad
        vm.jump_stack().push(vm.instruction_pointer()+2)

        func_start = get_func_from_directory(res)
        vm.set_instruction_pointer(func_start)
        init_memory(memory, res)
        assign_params(vm, memory, res)
        vm.clear_func_params()
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
    elif op == 'returnassignTODO':
        # returnassignTODO left  res
        res_address = memory.active_memory().find_address(res)
        res_value = vm.execution_stack().pop()
        memory.assign_value_to_address(res_value, res_address)
        vm.point_to_next_quad()
    else:
        breakpoint()
        quad.print()
        vm.point_to_next_quad()


def assign_params(vm, memory, func_id):
    params_to_assign = FuncDirectory[func_id]['params']
    where_params_are = vm.get_func_params()
    for i in range(0, len(params_to_assign)):
        address_to_fill = memory.active_memory(
        ).find_address(params_to_assign[i][1])
        value_to_fill_with = memory.get_value_from_address(
            where_params_are[i])
        memory.assign_value_to_address(value_to_fill_with, address_to_fill)
