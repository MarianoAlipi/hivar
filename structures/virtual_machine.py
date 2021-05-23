from structures.symbol_table import SymbolTable
from structures.stack import Stack
from execution import process_quad

# leave as global for easy access
st = SymbolTable.get()


class VirtualMachine:

    # used for singleton implementation
    __instance = None

    @classmethod
    def get(arg):
        if VirtualMachine.__instance is None:
            VirtualMachine()
        return VirtualMachine.__instance

    def instruction_pointer(self):
        return self.__ip

    def set_instruction_pointer(self, index):
        self.__ip = index - 1

    def point_to_next_quad(self):
        self.__ip = self.__ip + 1

    def execute_quads(self):
        quads = self.__quads
        while self.instruction_pointer() < len(quads):
            try:
                process_quad(self, quads[self.instruction_pointer()])
            except Exception as err:
                print('AAAAA', quads[self.instruction_pointer()].print(), err)
                breakpoint()

    def add_func_param(self, param):
        self.__func_params.append(param)

    def get_func_params(self):
        return self.__func_params

    def clear_func_params(self):
        self.__func_params = []

    def jump_stack(self):
        return self.__jump_stack

    def execution_stack(self):
        return self.__execution_stack

    def __init__(self):
        if VirtualMachine.__instance:
            raise Exception(
                "VirtualMachine already declared, use 'VirtualMachine.get()'")
        else:
            VirtualMachine.__instance = self
            self.__ip = 0
            self.__execution_stack = Stack()
            self.__quads = st.quads()
            self.__func_params = []
            self.__jump_stack = Stack()
