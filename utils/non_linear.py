
from structures.quadruples import Quad
from utils.exp import get_temp_var_name

# if else


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
    # We now know the target of the last gotof, so set it.
    last_gotof = st.pending_jumps().pop()
    last_gotof.set_res(len(st.quads()) + 1)


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
    if_escape.set_res(len(st.quads()) + 1)


# while

def fill_gotof_while(st):
    end = st.pending_jumps().pop()
    quad_to_return_to = st.pending_jumps().pop()
    quad = Quad('goto', None, None, quad_to_return_to)
    st.quads().append(quad)
    end.set_res(len(st.quads())+1)


def eval_while_exp(st):
    exp_type = st.op_types().pop()
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
    st.pending_jumps().push(len(st.quads()) + 1)


def restart_loop(st):
    counter_quad = Quad('+', 1, st.for_ids().top(), st.for_ids().top())
    st.quads().append(counter_quad)
    gotof_quad = st.pending_jumps().pop()
    go_back = st.pending_jumps().pop()
    quad = Quad('goto', None, None, go_back)
    st.quads().append(quad)
    gotof_quad.set_res(len(st.quads())+1)
    st.for_ids().pop()


def save_cond_for_quad(st):
    temp = get_temp_var_name(st)
    quad = Quad('<', st.for_ids().top(), st.operands().pop(), temp)
    st.quads().append(quad)
    st.pending_jumps().push(len(st.quads()))
    gotof_quad = Quad('gotof', temp, None, None)
    st.quads().append(gotof_quad)
    st.pending_jumps().push(gotof_quad)


def save_for_assgn_quad(st):
    exp_val = st.operands().pop()
    quad = Quad('=', exp_val, None, st.for_ids().top())
    st.quads().append(quad)

# main


def save_main_quad(st):
    gotomain_quad = st.pending_jumps().pop()
    gotomain_quad.set_res(len(st.quads()) + 1)


def assign_res_to_main_quad(st):
    gotomain_quad = Quad('goto', '', '', '')
    st.pending_jumps().push(gotomain_quad)
    st.quads().append(gotomain_quad)
