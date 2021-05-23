from structures.memory import Memory
from structures.func_directory import get_local_vars_from_id


def is_cte(operand):
    # boolean cte
    if operand == 'True' or operand == 'False':
        return True
    # char cte?
    # numeric cte
    return type(operand) == int or type(operand) == float


def init_memory(memory, func_id):
    new_vars = get_local_vars_from_id(func_id)
    global_mem = memory.get_global_memory()
    for var in new_vars:
        global_mem.init_address(var[0], var[1])


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
        # crear mnemoria local usando funcdir['local_vars'] tiene todas, las iteras y las creAS igUAL QUE como creamos las globales
        # pasar params, crear array params en virtual_machine guardar ahi en lo que sales del scope global y entras al local
        # protip: locales estan
        # vm.set_instruction_pointer(res)
        # return es como un params pero alrevez
    else:
        breakpoint()
        quad.print()
        vm.point_to_next_quad()
