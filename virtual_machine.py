from structures.stack import Stack

class VirtualMachine:

    __instance = None
    # For the time being, it only contains the quad number to return to
    # when the VM finds an 'endfunc'.
    __callstack = None

    # Look up the value of a variable in the current scope.
    def lookup_var(self, st, var):
        if isinstance(var, str):
            try:
                return st.current_scope().vars()[var]
            except KeyError:
                print(f'KeyError', end=' ')
                return 0
        return var

    def exec_plus(self, st, left, right, result):
        left = self.lookup_var(st, left)
        right = self.lookup_var(st, right)

        res = left + right
        st.current_scope().vars()[result] = res
        return res

    def exec_minus(self, st, left, right, result):
        left = self.lookup_var(st, left)
        right = self.lookup_var(st, right)

        res = left - right
        st.current_scope().vars()[result] = res
        return res

    def exec_mult(self, st, left, right, result):
        left = self.lookup_var(st, left)
        right = self.lookup_var(st, right)

        # TODO
        # Make sure the resulting value is int or float according to the
        # semantics cube?
        res = left * right
        st.current_scope().vars()[result] = res
        return res

    def exec_div(self, st, left, right, result):
        left = self.lookup_var(st, left)
        right = self.lookup_var(st, right)

        # TODO
        # Make sure the resulting value is int or float according to the
        # semantics cube?
        res = left / right
        st.current_scope().vars()[result] = res
        return res

    def exec_assignment(self, st, left, right, result):
        left = self.lookup_var(st, left)

        # If the operand is an ID, look up its value in the current scope.
        st.current_scope().vars()[result] = left
        return left

    def exec_write(self, st, left, right, result):
        res_str = ''
        for elem in result:
            res_str += elem
        print(res_str)
        return res_str

    actions = {
        '+': exec_plus,
        '-': exec_minus,
        '*': exec_mult,
        '/': exec_div,
        '=': exec_assignment,
        'write': exec_write
    }

    @classmethod
    def get(cls):
        if VirtualMachine.__instance is None:
            VirtualMachine()
        return VirtualMachine.__instance
        
    def __init__(self):
        if VirtualMachine.__instance:
            raise Exception(
                "Virtual Machine already instantiated, use 'VirtualMachine.get()'")
        else:
            VirtualMachine.__instance = self
            VirtualMachine.__callstack = Stack()

    # Execute the read quadruples.
    def execute(self, st):
        print('=> Virtual machine')

        curr_quad = 0
        while curr_quad >= 0 and curr_quad < len(st.quads()):

            quad = st.quads()[curr_quad]
            operator = quad.operator()
            left, right, result = quad.left_op(), quad.right_op(), quad.result()

            print(f'{(curr_quad + 1):03}  {operator}  {left}  {right}  {result}', end='  || ')

            if operator == 'goto':
                print(f'{operator}: {result}')
                curr_quad = result - 1
                continue
            elif operator == 'gosub':
                print(f'{operator}: {result}')
                self.__callstack.push(curr_quad + 1)
                curr_quad = result - 1
                # TODO
                # Change scope
                continue
            elif operator == 'endfunc':
                quad_to_return_to = self.__callstack.pop()
                print(f'{operator}: jump to {quad_to_return_to + 1}')
                curr_quad = quad_to_return_to
                # TODO
                # Change scope
                continue
            elif operator == 'param':
                # Do nothing (it's already handled).
                print(f'{operator}: already handled')
            else:
                try:
                    val = self.actions[operator](self, st, left, right, result)
                    print(f'{operator}: {val}')
                except:
                    print(f'{operator} not yet implemented. Skipping!')

            curr_quad += 1