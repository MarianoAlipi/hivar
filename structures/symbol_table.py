from collections import deque
from structures.stack import Stack
from structures.scope import Scope


class SymbolTable:

    # used for singleton implementation
    __instance = None

    @classmethod
    def get(arg):
        if SymbolTable.__instance is None:
            SymbolTable()
        return SymbolTable.__instance

    def current_scope_name(self):
        return self.scope_stack()[-1][0]

    def current_scope(self):
        return self.scope_stack()[-1][1]

    def scope_stack(self):
        return self.__scope_stack

    def set_curr_type(self, new_type):
        def is_valid():
            if new_type == 'int' or new_type == 'float' or new_type == 'char':
                return True
            if new_type in self.classes():
                return True
            #valid in functions
            if new_type == 'void':
                return True
            return False

        if is_valid():
            self.__current_type = new_type
        else:
            raise Exception(f"Invalid type: '{new_type}'.")

    def current_type(self):
        return self.__current_type

    def set_curr_id(self, new_id):
        self.__current_id = new_id

    def current_id(self):
        return self.__current_id

    def last_saved_func(self):
        return self.__last_saved_func

    def set_last_saved_func(self, saved_func):
        self.__last_saved_func = saved_func

    def save_var(self):
        if self.current_type() in self.classes():  # checks if its an object, if it is, then use special method
            global_scope = self.scope_stack()[0][1]
            self.current_scope().add_obj_var(
                global_scope, self.current_id(), self.current_type())
        else:
            self.current_scope().add_var(self.current_id(), self.current_type())

    def save_temp_var(self, name, var_type):
        self.current_scope().add_var(name, var_type)

    def save_func(self):
        scope = self.current_scope()
        saved_func = scope.add_func(self.current_id(), self.current_type())
        self.set_last_saved_func(saved_func)

    def save_parameter(self):
        self.last_saved_func().params().append((self.current_type(), self.current_id()))
        self.current_scope().add_var(self.current_id(), self.current_type())

    def push_scope(self):
        name = self.current_id()
        scope_obj = Scope()
        scope_obj.set_parent(self.current_scope())
        self.current_scope().scopes()[name] = scope_obj
        self.scope_stack().append((name, scope_obj))

    def pop_scope(self):
        self.scope_stack().pop()

    def constant_sign(self):
        return self.__constant_sign

    def set_constant_sign(self, new_sign):
        self.__constant_sign = new_sign

    def quads(self):
        return self.__quads

    def classes(self):
        return self.__classes

    def add_class(self, class_name):
        return self.__classes.append(class_name)

    # Temp variable counter
    def t_counter(self):
        return self.__t_counter

    def add_to_t_counter(self):
        self.__t_counter += 1

    def operands(self):
        return self.__operands

    def op_types(self):
        return self.__op_types

    def operators(self):
        return self.__operators

    def pending_jumps(self):
        return self.__pending_jumps

    # These are stacks of stacks.
    # When a ( is pushed, the current stacks are saved into these.
    # When ) is found, the previous stacks are retrieved by popping these.
    def operands_stacks(self):
        return self.__operands_stacks

    def types_stacks(self):
        return self.__types_stacks

    def operators_stacks(self):
        return self.__operators_stacks

    def if_escapes(self):
        return self.__if_escapes

    def for_ids(self):
        return self.__for_ids

    def set_operands(self, val):
        self.__operands = val

    def set_types(self, val):
        self.__op_types = val

    def set_operators(self, val):
        self.__operators = val

    def print_quads(self):
        quads = self.quads()
        counter = 1
        for quad in quads:

            print(counter, quad.operator(), quad.left_op(),
                  quad.right_op(), quad.result())
            counter += 1

    def var_to_assign(self):
        return self.__var_to_assign

    def current_params(self):
        return self.__current_params

    def reset_current_params(self):
        self.__current_params = []

    def __init__(self):
        if SymbolTable.__instance:
            raise Exception(
                "Symbol Table already declared, use 'SymbolTable.get()'.")
        else:
            SymbolTable.__instance = self
            self.__scope_stack = deque()
            self.__scope_stack.append(('global', Scope()))
            self.__current_type = None
            self.__current_id = None
            self.__last_saved_func = None
            self.__constant_sign = '+'
            self.__operands = Stack()
            self.__op_types = Stack()
            self.__operators = Stack()
            self.__pending_jumps = Stack()
            self.__operands_stacks = Stack()
            self.__types_stacks = Stack()
            self.__operators_stacks = Stack()
            self.__quads = []
            self.__classes = []
            self.__t_counter = 1
            self.__if_escapes = Stack()
            self.__var_to_assign = Stack()
            self.__for_ids = Stack()
            self.__current_params = []
