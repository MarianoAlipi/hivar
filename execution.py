from structures.memory import Memory, MemoryChunk
from structures.func_directory import get_local_vars_from_id, FuncDirectory


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
            # TODO: check init_address because it's hardcoded to 'global' memory ranges
            local_mem.init_address(var[0], var[1], 'local')
        memory.get_locals_stack().push(local_mem)


def process_quad(vm, quad):
    op, left, right, res = quad.unpack()

    memory = Memory.get()
    global_mem = memory.get_global_memory()
    if op == '=':
        if is_cte(left):
            global_mem.set_cte_val_for_id(res, left)
        else:
            global_mem.set_val_for_id(res, left)
        vm.point_to_next_quad()
    elif op in ['+', '-', '/', '*', '<', '>', '==', '!=', '<=', '>=', '&&', '||']:
        global_mem.solve_quad(op, res, left, right)
        vm.point_to_next_quad()
    elif op == 'goto':
        vm.set_instruction_pointer(res)
    elif op == 'gotomain':
        vm.set_instruction_pointer(res)
        init_memory(memory, 'global')
    elif op == 'gotof':
        comparison_value = global_mem.get_value(left)
        if comparison_value == False:
            vm.set_instruction_pointer(res)
        else:
            vm.point_to_next_quad()
    elif op == 'write':
        print(global_mem.get_value(res[0]))
        vm.point_to_next_quad()
    elif op == 'read':
        user_input = input('>>> ')
        global_mem.set_cte_val_for_id(res, user_input)
        vm.point_to_next_quad()
    elif op == 'gosub':
        # TODO
        # crear mnemoria local usando funcdir['local_vars'] tiene todas, las iteras y las creAS igUAL QUE como creamos las globales
        # pasar params, crear array params en virtual_machine guardar ahi en lo que sales del scope global y entras al local
        # protip: locales estan
        # vm.set_instruction_pointer(res)
        # return es como un params pero alrevez

        vm.set_instruction_pointer(res)
        # TODO: find the func_id in a more efficient way
        func_id = ''
        for key in FuncDirectory:
            if FuncDirectory[key]['dir'] == res:
                func_id = res
        
        if func_id == '':
            raise Exception('Function at address {res} not found in FuncDirectory.')

        vm.set_func_params(FuncDirectory[func_id]['params'])
        init_memory(memory, func_id)
    elif op == 'return':
        # TODO: all of this
        # How to get func_id?
        vm.set_func_params(FuncDirectory[func_id]['params'])
    else:
        breakpoint()
        quad.print()
        vm.point_to_next_quad()
