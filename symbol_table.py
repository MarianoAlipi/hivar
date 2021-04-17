##########################
## internal use classes ##
##########################

class Variable:
    def __init__(self, name, var_type):
        self.__name = name
        self.__type = var_type
        self.__value = None

    def name(self):
        return self.__name

    def var_type(self):
        return self.__type

    def value(self):
        return self.__value


class Function:
    def __init__(self, name, func_type, parameters=[]):
        self.__name = name
        self.__type = func_type
        self.__params = parameters  # list of variables?

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

    def funcs(self):
        return self.__funcs

    def vars(self):
        return self.__vars

    def func(self, func_name):
        if func_name in self.funcs():
            return self.funcs()[func_name]
        return None

    def var(self, var_name):
        if var_name in self.vars():
            return self.vars()[var_name]
        return None

    def add_func(self, new_name, func_type=None):
        if new_name in self.funcs():
            # return False for now, how do we manage errors?
            print(
                f'Function "{new_name}" is already declared in this scope')
            return False
        self.__funcs[new_name] = Function(new_name, func_type)
        return self.__funcs[new_name]

    def add_var(self, new_name, var_type=None):
        if new_name in self.vars():
            # return False for now, how do we manage errors?
            print(
                f'Variable "{new_name}" is already declared in this scope')
            return False
        self.__vars[new_name] = Variable(new_name, var_type)

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

    def scopes(self):
        return self.__scopes

    def set_curr_scope(self, new_scope):
        self.__current_scope = new_scope
        
    def current_scope(self):
        return self.__current_scope

    def set_curr_type(self, new_type):
        self.__current_type = new_type

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

    # TODO
    # If current_rows and/or current_cols have a value,
    # save the variable as an array/matrix.
    def save_var(self):
        self.current_scope().add_var(self.current_id(), self.current_type())
        self.set_curr_rows(None)
        self.set_curr_cols(None)

    def save_func(self):
        scope = self.current_scope()
        saved_func = scope.add_func(self.current_id(), self.current_type())
        self.set_last_saved_func(saved_func)

    def save_parameter(self):
        param = Variable(self.current_id(), self.current_type())
        self.last_saved_func().params().append(param)

    def set_val(self, new_val):
        self.__val = new_val

    def val(self):
        return self.__val

    # TODO: refactor (see pop_scope() below)
    def push_scope(self):
        pass

    # TODO
    # Stack/list of tuples [ ('global', Scope()), ('pelos', Scope()), ('foo', Scope()) ]
    # Key is the name of the class/function/scope
    # each scope would have a dictionary of contained scopes:
    # (global:) scopes = {'pelos': Scope()}
    # (pelos:) scopes = {'foo': Scope(), 'bar': Scope()}
    def pop_scope(self):
        pass

    def __init__(self):
        if SymbolTable.__instance:
            # return False for now, how do we manage errors?
            print(
                "Symbol Table already declared, use 'SymbolTable.get()'")
            return False
        else:
            SymbolTable.__instance = self
            self.__scopes = {'global': Scope()}
            self.__current_scope = self.scopes()['global']
            self.__current_type = None
            self.__current_id = None
            self.__last_saved_func = None
            self.__current_rows = None
            self.__current_cols = None
            self.__val = None
