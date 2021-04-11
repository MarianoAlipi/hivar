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
    def __init__(self, name, func_type):
        self.__name = name
        self.__type = func_type

    def name(self):
        return self.__name

    def return_type(self):
        return self.__type


class Scope:
    def __init__(self, name):
        self.__name = name
        self.__funcs = {}
        self.__vars = {}

    def name(self):
        return self.__name

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

    def add_var(self, new_name, var_type=None):
        if new_name in self.vars():
            # return False for now, how do we manage errors?
            print(
                f'Variable "{new_name}" is already declared in this scope')

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

    def __init__(self):
        if SymbolTable.__instance:
            # return False for now, how do we manage errors?
            print(
                "Symbol Table already declared, use 'SymbolTable.get()'")
            return
        else:
            SymbolTable.__instance = self
            self.scopes = {'global': {}}
