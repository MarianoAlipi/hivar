from collections import deque
from structures.stack import Stack

##########################
## internal use classes ##
##########################


class Variable:
    def __init__(self, name, var_type, rows=0, cols=0):
        self.__name = name
        self.__type = var_type
        self.__value = [[]]
        self.__rows = rows
        self.__cols = cols
        for r in range(rows):
            for _ in range(cols):
                self.__value[r].append([])
            self.__value.append([])
        self.__value.remove([])

    def name(self):
        return self.__name

    def var_type(self):
        return self.__type

    def value(self, rows=0, cols=0):
        # value is a single value inside a [[]] or a dict in case of objects
        return self.__value[rows][cols]

    def rows(self):
        return self.__rows

    def cols(self):
        return self.__cols

    def set_value(self, new_val, rows=0, cols=0):
        self.__value[rows][cols] = new_val

    def set_attr_value(self, attr, new_val, rows=0, cols=0):
        try:
            self.__value[rows][cols][attr] = new_val
        except Exception as err:
            raise Exception(f"oops @set_attr_value: {err}")


class Function:
    def __init__(self, name, func_type, parameters=[]):
        self.__name = name
        self.__type = func_type
        self.__params = parameters

    def name(self):
        return self.__name

    def return_type(self):
        return self.__type

    def params(self):
        return self.__params


class Scope:
    def __init__(self):
        self.__funcs = {}
        self.__vars = {}
        self.__scopes = {}
        self.__attributes = []

    def funcs(self):
        return self.__funcs

    def vars(self):
        return self.__vars

    def scopes(self):
        return self.__scopes

    def attributes(self):
        return self.__attributes

    def func(self, func_name):
        if func_name in self.funcs():
            return self.funcs()[func_name]
        else:
            raise Exception(
                f'Function "{func_name}" not found')

    def var(self, var_name):
        if var_name in self.vars():
            return self.vars()[var_name]
        else:
            raise Exception(
                f'Variable "{var_name}" not found')

    def add_func(self, new_name, func_type=None):
        if new_name in self.funcs():
            raise Exception(
                f'Function "{new_name}" is already declared in this scope')
        self.__funcs[new_name] = Function(new_name, func_type)
        return self.__funcs[new_name]

    def add_var(self, new_name, var_type=None, rows=1, cols=1):
        if new_name in self.vars():
            raise Exception(
                f'Variable "{new_name}" is already declared in this scope')
        self.__vars[new_name] = Variable(new_name, var_type, rows, cols)

    def add_attribute(self, attr):
        self.__attributes.append(attr)

    def get_var_from_id(self, var_id):
        breakpoint()
        if var_id in self.vars():
            return self.vars()[var_id]
        else:
            # TODO: busca más arriba
            raise Exception(
                f'Can not find variable "{var_id}"')

    def set_vars_as_attrs(self):
        for var in self.vars():
            self.add_attribute(var)


##########################
## external use classes ##
##########################


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
            raise Exception(f"Invalid type: {new_type}")

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

    def set_curr_rows(self):
        self.__current_rows = self.val()

    def current_rows(self):
        return self.__current_rows

    def set_curr_cols(self):
        self.__current_cols = self.val()

    def current_cols(self):
        return self.__current_cols

    def set_rows_cols_to_none(self):
        self.__current_cols = None
        self.__current_rows = None

    def save_var(self):
        generic_types = ['int', 'float', 'char']
        if self.current_type() in generic_types:
            # check for array
            if self.current_rows():
                # check for matrix
                if self.current_cols():
                    self.current_scope().add_var(self.current_id(), self.current_type(),
                                                 self.current_rows(), self.current_cols())
                else:
                    self.current_scope().add_var(self.current_id(),
                                                 self.current_type(), self.current_rows())
            else:
                self.current_scope().add_var(self.current_id(), self.current_type())
        else:
            if self.current_rows():
                if self.current_cols():
                    self.current_scope().add_var(self.current_id(), self.current_type(),
                                                 self.current_rows(), self.current_cols())
                else:
                    self.current_scope().add_var(self.current_id(),
                                                 self.current_type(), self.current_rows())
            else:
                self.current_scope().add_var(self.current_id(), self.current_type())
            # init the object with all attributes in none
            class_scope = self.scope_stack()[0][1].scopes()[
                self.current_type()]
            attrs = {}
            for attr in class_scope.attributes():
                attrs[attr] = None
            var = self.current_scope().get_var_from_id(self.current_id())

            # if its an array init all the objects
            if self.current_rows():
                if self.current_cols():
                    for r in range(self.current_rows()):
                        for c in range(self.current_cols()):
                            var.set_value(attrs, r, c)
                else:
                    for r in range(self.current_rows()):
                        var.set_value(attrs, r)
            else:
                var.set_value(attrs)

    def save_func(self):
        scope = self.current_scope()
        saved_func = scope.add_func(self.current_id(), self.current_type())
        self.set_last_saved_func(saved_func)

    def save_parameter(self):
        param = Variable(self.current_id(), self.current_type())
        self.last_saved_func().params().append(param)
        self.current_scope().add_var(self.current_id(), self.current_type())

    def set_val(self, new_val):
        self.__val = new_val

    def val(self):
        return self.__val

    def push_scope(self):
        name = self.current_id()
        scope_obj = Scope()
        self.current_scope().scopes()[name] = scope_obj
        self.scope_stack().append((name, scope_obj))

    def pop_scope(self):
        self.scope_stack().pop()

    def operands(self):
        return self.__operands

    def op_types(self):
        return self.__op_types

    def operators(self):
        return self.__operators

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

    def var_to_assign(self):
        return self.__var_to_assign

    def set_var_to_assign(self):
        var_to_assign = self.__current_id
        # check if its an object
        if self.current_attribute_id():
            var_to_assign += '.' + self.current_attribute_id()
        if self.current_rows() > 1:
            var_to_assign += f'[{self.current_rows()}]'
            if self.current_cols() > 1:
                var_to_assign += f'[{self.current_cols()}]'
        self.__var_to_assign = var_to_assign

    def current_result(self):
        return self.__current_result

    def set_current_result(self, res):
        breakpoint()
        self.__current_result = res

    def current_attribute_id(self):
        return self.__current_attribute

    def set_curr_attribute(self, attr_id):
        breakpoint()
        var = self.current_scope().get_var_from_id(self.current_id())
        if attr_id is None:
            self.__current_attribute = attr_id
        elif type(var.value()) is dict:
            if attr_id in var.value():
                self.__current_attribute = attr_id
        else:
            raise Exception(
                f"var {var.name()} does not have attribute {attr_id}, existing vars: {var.value()}")

    def assign_res(self):
        target = self.var_to_assign()
        rows = cols = 0
        # checks for object
        if '.' in target:
            var_id = target[:target.find('.')]
            attr = target[target.find('.')+1:target.find('[')]
            # checks for matrix
            if '][' in target:
                rows = int(target[target.find('[')+1:target.find(']')])
                cols = int(target[target.find(']')+2:-1])
            elif '[' in target:
                rows = int(target[target.find('[')+1:-1])

            # TODO
            current_attribute_type = 'TODO'
            var = self.current_scope().get_var_from_id(var_id)
            if current_attribute_type == type(self.current_result()):
                var.set_attr_value(attr, self.current_result(), rows, cols)
            else:
                raise Exception(
                    f"types dont match, cant assign var {var.name()} attr type = {current_attribute_type}, current result type = {type(self.current_result())} ")
        else:
            var_id = target[:target.find('[')]
            # checks for matrix
            if '][' in target:
                rows = int(target[target.find('[')+1:target.find(']')])
                cols = int(target[target.find(']')+2:-1])
            elif '[' in target:
                rows = int(target[target.find('[')+1:-1])
            var = self.current_scope().get_var_from_id(var_id)
            if var.var_type() == type(self.current_result()):
                var.set_value(self.current_result(), rows, cols)
            else:
                raise Exception(
                    f"types dont match, cant assign var {var.name()} type = {var.var_type()}, current result type = {type(self.current_result())} ")

    def __init__(self):
        if SymbolTable.__instance:
            raise Exception(
                "Symbol Table already declared, use 'SymbolTable.get()'")
        else:
            SymbolTable.__instance = self
            self.__scope_stack = deque()
            self.__scope_stack.append(('global', Scope()))
            self.__current_type = None
            self.__current_id = None
            self.__last_saved_func = None
            self.__current_rows = None
            self.__current_cols = None
            self.__val = None
            self.__operands = Stack()
            self.__op_types = Stack()
            self.__operators = Stack()
            self.__constant_sign = '+'
            self.__quads = Stack()
            self.__classes = []
            self.__var_to_assign = None
            self.__current_result = None
            self.__current_attribute = None
