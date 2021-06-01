# function used for quad generation for non-linear expressions and jumps
from structures.quadruples import Quad
from structures.semantics_cube import BOOL
from utils.exp import get_temp_var_name
from structures.func_directory import set_starting_quad_to_func, get_return_var_id


###
# functions for if else handling
###


def create_gotof(st):
    exp_type = st.op_types().pop()
    # Make sure the condition evaluates to a boolean.
    if exp_type != 'bool':
        raise Exception(
            f'Type mismatch. \
            Expected bool but expression resolved to {exp_type}.'
        )
    else:
        exp_eval = st.operands().pop()
        # Generate the gotof quad
        gotof_quad = Quad('gotof', exp_eval, None, None)
        # Add gotof quad to pending_jumps (we don't know its target quad yet)
        # and to the list of all quads.
        st.pending_jumps().push(gotof_quad)
        st.quads().append(gotof_quad)


def create_goto(st):
    # This is the end of the block, so we'll need to insert an if_escape here.
    if_escape = st.if_escapes().top()
    st.quads().append(if_escape)


def fill_gotof(st):
    last_gotof = st.pending_jumps().pop()
    last_gotof.set_res(len(st.quads()) + 2)


def create_if_escape(st):
    # 'if_escape' is a goto that jumps out of the whole conditional structure.
    # There is one 'master' if_escape for each conditional structure
    # (i.e. the whole if-elsif-else block).
    # Here we create the 'master' if_escape that will be inserted as many times
    # as needed.
    if_escape = Quad('goto', None, None, None)
    st.if_escapes().push(if_escape)


def decision_end(st):
    # Set the pending gotos' result.
    # Because we use the object's reference,
    # the result will be in every relevant quad.
    if_escape = st.if_escapes().pop()
    st.quads().append(if_escape)
    if_escape.set_res(len(st.quads()) + 1)


###
# functions for while handling
###

def fill_gotof_while(st):
    # end is a gotof quad indicating where the function ends
    end = st.pending_jumps().pop()
    quad_to_return_to = st.pending_jumps().pop()
    quad = Quad('goto', None, None, quad_to_return_to)
    st.quads().append(quad)
    end.set_res(len(st.quads())+1)


def eval_while_exp(st):
    exp_type = st.op_types().pop()
    # Make sure the condition evaluates to a boolean.
    if exp_type != 'bool':
        raise Exception(
            f'Type mismatch. \
            Expected bool but expression resolved to {exp_type}.'
        )
    else:
        exp_eval = st.operands().pop()
        # Generate the gotof quad
        gotof_quad = Quad('gotof', exp_eval, None, None)
        # Add gotof quad to pending_jumps (we don't know its target quad yet)
        # and to the list of all quads.
        st.pending_jumps().push(gotof_quad)
        st.quads().append(gotof_quad)


def push_while(st):
    # save current position to get back later
    st.pending_jumps().push(len(st.quads()) + 1)


def restart_loop(st):
    # runs every time a for loop iterates, it increases 1 to the counter
    counter_quad = Quad('+', 1, st.for_ids().top(), st.for_ids().top())
    st.quads().append(counter_quad)
    gotof_quad = st.pending_jumps().pop()
    # it creates goto quad that goes to the condition evaluation
    go_back = st.pending_jumps().pop()
    quad = Quad('goto', None, None, go_back)
    st.quads().append(quad)
    # it lets the gotof quad know where to resume
    gotof_quad.set_res(len(st.quads())+1)
    # finally, it removes the for id
    st.for_ids().pop()


def save_cond_for_quad(st):
    # creates the evaluation quad for the for loop and the gotof quad in case of break
    temp = get_temp_var_name(st, BOOL)
    st.current_scope().add_var(temp, BOOL)
    quad = Quad('<', st.for_ids().top(), st.operands().pop(), temp)
    st.quads().append(quad)
    st.pending_jumps().push(len(st.quads()))
    gotof_quad = Quad('gotof', temp, None, None)
    st.quads().append(gotof_quad)
    st.pending_jumps().push(gotof_quad)


def save_for_assgn_quad(st):
    # creates assignation quad for initial declaration in for loop
    exp_val = st.operands().pop()
    quad = Quad('=', exp_val, None, st.for_ids().top())
    st.quads().append(quad)


###
# functions for main jumps handling
###


def assign_res_to_main_quad(st):
    # sets the starting quad for main routine and saves its spot to func directory
    gotomain_quad = st.pending_jumps().pop()
    gotomain_quad.set_res(len(st.quads()) + 1)
    set_starting_quad_to_func('global', len(st.quads()) + 1)


def save_main_quad(st):
    # creates go to main quad and stores it for when we find the start
    gotomain_quad = Quad('gotomain', '', '', '')
    st.pending_jumps().push(gotomain_quad)
    st.quads().append(gotomain_quad)


###
# functions for func call handling
###


def save_func_call_operand(st):
    # saves function return var in operand stack
    st.operands().push(get_return_var_id(st.current_scope_name()))
    # saves return var as current
    curr_var = st.current_scope().get_var_from_id(
        get_return_var_id(st.current_scope_name()))
    # saves return var type in op_types stack
    st.op_types().push(curr_var.var_type())
