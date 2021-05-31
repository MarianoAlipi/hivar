def valid(self):
    if len(self.stack()) <= 0:
        raise Exception(
            "stack is empty")
    return True


def is_empty(self):
    if len(self.stack()) == 0:
        return True
    return False


def push_operator(st, op):
    if op == '(': #handling for false bottom
        st.operands_stacks().push(st.operands())
        st.set_operands(Stack())

        st.types_stacks().push(st.op_types())
        st.set_types(Stack())

        st.operators_stacks().push(st.operators())
        st.set_operators(Stack())
    else:
        st.operators().push(op)


def pop_operator(st, op):
    if op == ')':#handling for false bottom removal
        try:
            prev_operands = st.operands_stacks().pop()
            st.set_operands(prev_operands)
        except:
            st.set_operands(Stack())

        try:
            prev_types = st.types_stacks().pop()
            st.set_types(prev_types)
        except:
            st.set_types(Stack())

        try:
            prev_operators = st.operators_stacks().pop()
            st.set_operators(prev_operators)
        except:
            st.set_operators(Stack())
    else:
        st.operators().pop()


class Stack:

    def get_second(self):
        return self.__stack[-2]

    def __init__(self):
        self.__stack = []

    def stack(self):
        return self.__stack

    def push(self, val):
        self.__stack.append(val)

    def pop(self):
        if valid(self):
            element = self.__stack.pop()
            return element

    def top(self):
        if is_empty(self):
            return None
        return self.__stack[-1]
