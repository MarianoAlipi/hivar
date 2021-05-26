from collections import deque
from structures.stack import Stack

SIZE = 1000

ranges = {
    'global': {
        'int': SIZE*1, 'float': SIZE*2, 'bool': SIZE*3, 'char': SIZE*4
    },
    'local': {
        'int': SIZE*5, 'float': SIZE*6, 'bool': SIZE*7, 'char': SIZE*8
    },
    'temp': {
        'int': SIZE*9, 'float': SIZE*10, 'bool': SIZE*11, 'char': SIZE*12
    },
    'cte': {
        'int': SIZE*13, 'float': SIZE*14, 'bool': SIZE*15, 'char': SIZE*16
    },
}

literal_memory = {}

# from structures.memory import print_literal_memory, literal_memory


def print_literal_memory():
    print(literal_memory)


class MemoryChunk:
    def __init__(self, memory_size=SIZE):
        self.__int = {}
        self.__float = {}
        self.__bool = {}
        self.__char = {}
        self.__memory_left = {
            'int': memory_size, 'float': memory_size, 'bool': memory_size, 'char': memory_size}

    def get_vars(self, address_type):
        if address_type == 'int':
            return self.__int
        if address_type == 'float':
            return self.__float
        if address_type == 'bool':
            return self.__bool
        if address_type == 'char':
            return self.__char

    def find_address(self, var_id):
        ints = self.get_vars('int')
        if var_id in ints:
            return ints[var_id]

        floats = self.get_vars('float')
        if var_id in floats:
            return floats[var_id]

        bools = self.get_vars('bool')
        if var_id in bools:
            return bools[var_id]

        chars = self.get_vars('char')
        if var_id in chars:
            return chars[var_id]

        memory = Memory.get()
        constants = memory.get_constants()
        address = constants.find_address(var_id)
        return address

    def init_address(self, var_id, address_type, scope):
        try:
            # consige el arr de ese tipo
            assigned_address = self.get_vars(address_type)

            # ponle de valor, la direccion de memoria
            memory_index = ranges[scope][address_type]
            assigned_address[var_id] = memory_index

            # sube el index de la dir de memoria
            ranges[scope][address_type] = memory_index + 1

            # seteala vacia pq solo las famos de alta
            literal_memory[memory_index] = None
        except Exception as err:
            print(err)
            breakpoint()
        self.__memory_left[address_type] -= 1
        if self.__memory_left[address_type] <= 0:
            raise Exception(f'OUT OF MEMORY. type = {address_type}')

    def set_val_for_id(self, res_id, value_id):
        address_to_set = self.find_address(res_id)
        value_address = self.find_address(value_id)
        literal_memory[address_to_set] = literal_memory[value_address]

    def set_cte_val_for_id(self, res_id, value):
        address = self.find_address(res_id)
        literal_memory[address] = value

    def print(self):
        ints = self.get_vars('int')
        print('ints', ints)
        floats = self.get_vars('float')
        print('floats', floats)
        bools = self.get_vars('bool')
        print('bools', bools)
        chars = self.get_vars('char')
        print('chars', chars)

    def get_value(self, var_id):
        address = self.find_address(var_id)
        if not address:
            memory = Memory.get()
            constants = memory.get_constants()
            constant_value = constants.get_value(var_id)
            return constant_value
        return literal_memory[address]

    def solve_quad(self, operator, result_var, left_var, right_var):
        left_value = self.get_value(left_var)
        right_value = self.get_value(right_var)

        if operator == '+':
            result_value = left_value + right_value
        if operator == '-':
            result_value = left_value - right_value
        if operator == '*':
            result_value = left_value * right_value
        if operator == '/':
            result_value = left_value / right_value
        if operator == '<':
            result_value = left_value < right_value
        if operator == '>':
            result_value = left_value > right_value
        if operator == '==':
            result_value = left_value == right_value
        if operator == '!=':
            result_value = left_value != right_value
        if operator == '>=':
            result_value = left_value >= right_value
        if operator == '<=':
            result_value = left_value <= right_value
        if operator == '&&':
            result_value = left_value and right_value
        if operator == '||':
            result_value = left_value or right_value

        result_address = self.find_address(result_var)
        literal_memory[result_address] = result_value


class Memory:

    # used for singleton implementation
    __instance = None

    @classmethod
    def get(arg):
        if Memory.__instance is None:
            Memory()
        return Memory.__instance

    def get_global_memory(self):
        return self.__global

    def get_constants(self):
        return self.__ctes

    def add_constant(self, constant, constant_type):
        ctes = self.get_constants()
        ctes.init_address(constant, constant_type, 'global')
        ctes.set_cte_val_for_id(constant, constant)

    def locals_memory_stack(self):
        return self.__locals

    def active_memory(self):
        return self.locals_memory_stack().top()

    def get_value_from_address(self, address):
        try:
            return literal_memory[address]
        except:
            raise Exception(
                f"accessing empty memory address {address}")

    def assign_value_to_address(self, value, address):
        try:
            literal_memory[address] = value
        except:
            raise Exception(
                f"assigning empty memory address {address}")

    def __init__(self):
        if Memory.__instance:
            raise Exception(
                "Memory already declared, use 'Memory.get()'")
        else:
            Memory.__instance = self
            self.__global = MemoryChunk()
            self.__ctes = MemoryChunk()
            self.__locals = Stack()
            self.__locals.push(self.__global)
