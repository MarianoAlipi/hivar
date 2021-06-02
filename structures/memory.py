from collections import deque
from structures.stack import Stack
from utils.runtime import has_dimensions, is_cte
from structures.index_handler import matrix_index, array_index
SIZE = 1000

# assigns inital memory addresses
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

# the keys will be the literal memory values, there are no scope distinctions (as in real memory)
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

    def find_dim_address(self, var_id, look_deeper=True):
        # search in local scope
        ints = self.get_vars('int')
        if var_id in ints:
            return ints[var_id], 'int'

        floats = self.get_vars('float')
        if var_id in floats:
            return floats[var_id], 'float'

        bools = self.get_vars('bool')
        if var_id in bools:
            return bools[var_id], 'bool'

        chars = self.get_vars('char')
        if var_id in chars:
            return chars[var_id], 'char'

        # if it didnt find it in local scope, check the constants and global
        if look_deeper:
            memory = Memory.get()
            global_mem = memory.get_global_memory()
            address, address_type = global_mem.find_dim_address(var_id, False)
            if not address:
                raise Exception(
                    f"couldn't find dim address for var {var_id}")
            return address, address_type
        return None, None

    def find_object_address(self, var_id):
        attr_id = var_id[1]
        return self.find_address(attr_id)

    def find_address(self, var_id, search_deeper=True):
        # for objects look for the attribute
        if type(var_id) == tuple:
            return self.find_address(var_id[1])

        try:
            has_dims = has_dimensions(var_id)
        except Exception:
            has_dims = False

        # if it has dims, it finds the value of the arr variable, and then finds the index
        if has_dims:
            base, var_type = self.find_dim_address(var_id)
            if type(has_dims) == tuple:  # if it's a matrix
                mat_index = matrix_index().pop()
                row = mat_index[0]
                col = mat_index[1]
                return base + (has_dims[1] * row) + col, var_type
            else:  # if it's an array
                offset = array_index().pop()
                if is_cte(offset):
                    return base + offset, var_type
                else:
                    offset_value, var_type = self.find_address(offset)
                    offset_value = literal_memory[offset_value]
                    return base + offset_value, var_type

        # if it doesnt have dims, do a simple lookup
        ints = self.get_vars('int')
        if var_id in ints:
            return ints[var_id], 'int'

        floats = self.get_vars('float')
        if var_id in floats:
            return floats[var_id], 'float'

        bools = self.get_vars('bool')
        if var_id in bools:
            return bools[var_id], 'bool'

        chars = self.get_vars('char')
        if var_id in chars:
            return chars[var_id], 'char'

        # if it didnt find it in the vars, check the constants
        if search_deeper:
            memory = Memory.get()
            constants = memory.get_constants()
            address, var_type = constants.find_address(var_id, False)
            if not address:
                global_mem = memory.get_global_memory()
                address, var_type = global_mem.find_address(var_id, False)
                if not address:
                    raise Exception(
                        f"couldn't find address for var {var_id}")
            return address, var_type
        raise Exception(f"couldn't find address for var {var_id}")

    def init_object(self, var_id, address_type, scope):
        # WIP
        try:
            # gets the vars from that type
            assigned_address = self.get_vars(address_type)
            # the index is the base memory address and we set it to the address
            memory_index = ranges[scope][address_type]
            assigned_address[var_id] = memory_index

            # attrs = get_attributes()

            # por cada attr quita un memory_index y asigna none a la literal:memory
            for _ in range(attrs):
                memory_index = memory_index+1
                ranges[scope][address_type] = memory_index
                literal_memory[memory_index] = None

        except Exception as err:
            print(err)
        self.__memory_left[address_type] -= 1
        if self.__memory_left[address_type] <= 0:
            raise Exception(f'OUT OF MEMORY. type = {address_type}')

    def init_array(self, var_id, address_type, scope, var_size):
        try:
            # get the vars that are that type
            assigned_address = self.get_vars(address_type)
            # the index is the base memory address and we set it to the address
            memory_index = ranges[scope][address_type]
            assigned_address[var_id] = memory_index
            # for each variable set one more to the index and assign the space to literal memory
            for _ in range(var_size):
                memory_index = memory_index+1
                ranges[scope][address_type] = memory_index
                literal_memory[memory_index] = None

        except Exception as err:
            print(err)

        # set new array size and chec that there's still space
        self.__memory_left[address_type] -= var_size
        if self.__memory_left[address_type] <= 0:
            raise Exception(f'OUT OF MEMORY. type = {address_type}')

    def init_address(self, var_id, address_type, scope):
        try:
            # get the vars that are that type
            assigned_address = self.get_vars(address_type)
            # the index is the base memory address and we set it to the address
            memory_index = ranges[scope][address_type]
            assigned_address[var_id] = memory_index
            # set the new index in memory
            ranges[scope][address_type] = memory_index + 1
            # init as empty, fill later
            literal_memory[memory_index] = None
        except Exception as err:
            print(err)
        self.__memory_left[address_type] -= 1
        if self.__memory_left[address_type] <= 0:
            raise Exception(f'OUT OF MEMORY. type = {address_type}')

    def set_val_for_id(self, res_id, value_id):
        value_address, _ = self.find_address(value_id)
        address_to_set, _ = self.find_address(res_id)
        literal_memory[address_to_set] = literal_memory[value_address]

    def set_cte_val_for_id(self, res_id, value, value_type=None):
        if value_type == None:
            address, _ = self.find_address(res_id)
            literal_memory[address] = value
        else:
            address, var_type = self.find_address(res_id)
            if value_type == var_type:
                literal_memory[address] = value
            else:
                raise Exception(
                    f'Type mismatch: unable to assign {value} of type {value_type} to ID {res_id} of type {var_type}.'
                    )

    def print(self):
        # internal method, used for debugging
        ints = self.get_vars('int')
        print('ints', ints)
        floats = self.get_vars('float')
        print('floats', floats)
        bools = self.get_vars('bool')
        print('bools', bools)
        chars = self.get_vars('char')
        print('chars', chars)

    def get_value(self, var_id):
        address, _ = self.find_address(var_id)
        if not address:
            # if theres no address, then it's a constant, get value from there
            memory = Memory.get()
            constants = memory.get_constants()
            constant_value = constants.get_value(var_id)
            return constant_value
        return literal_memory[address]

    def solve_quad(self, operator, result_var, left_var, right_var):
        right_value = self.get_value(right_var)
        left_value = self.get_value(left_var)

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

        result_address, _ = self.find_address(result_var)
        literal_memory[result_address] = result_value


class Memory:

    # used for singleton implementation
    __instance = None

    @ classmethod
    def get(arg):
        if Memory.__instance is None:
            Memory()
        return Memory.__instance

    def get_global_memory(self):
        return self.__global

    def get_constants(self):
        return self.__ctes

    def add_constant(self, constant, constant_type):
        # constants are always in the global scope so that they can be available from anywhere
        ctes = self.get_constants()
        ctes.init_address(constant, constant_type, 'global')
        ctes.set_cte_val_for_id(constant, constant)

    def locals_memory_stack(self):
        return self.__locals

    def active_memory(self):
        # most recent memory in the stack
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
