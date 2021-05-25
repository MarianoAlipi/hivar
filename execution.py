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
        return global_mem
    else:
        local_mem = MemoryChunk()
        for var in new_vars:
            local_mem.init_address(var[0], var[1], 'local')
        return local_mem


def process_quad(vm, quad):
    op, left, right, res = quad.unpack()

    memory = Memory.get()
    try:
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
            breakpoint()

        # TODOWRITE checar si es un banner (solo print) o si es un val (consulta)
            print(memory.active_memory().get_value(res[0]))
            breakpoint()
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
        elif op == 'returnassignTODO':
            # returnassignTODO left  res
            res_address = memory.active_memory().find_address(res)
            res_value = vm.execution_stack().pop()
            memory.assign_value_to_address(res_value, res_address)
            vm.point_to_next_quad()
        elif op == 'verify':
            res_value = memory.active_memory().get_value(left)
            if res_value >= res:
                raise Exception(
                    f'Out of bounds: {left} has a value of {res_value}, ' +
                    f'must be between 0 and {res}')
            vm.point_to_next_quad()
        elif op == 'ASSGN':
            breakpoint()
            vm.point_to_next_quad()
        else:
            breakpoint()
            quad.print()
            vm.point_to_next_quad()
    except Exception as err:
        quad.print()
        print('error en process_quad:', err)
        breakpoint()


def assign_params(vm, memory, func_id):
    params_to_assign = FuncDirectory[func_id]['params']
    where_params_are = vm.get_func_params()
    for i in range(0, len(params_to_assign)):
        address_to_fill = memory.active_memory(
        ).find_address(params_to_assign[i][1])
        value_to_fill_with = memory.get_value_from_address(
            where_params_are[i])
        memory.assign_value_to_address(value_to_fill_with, address_to_fill)
