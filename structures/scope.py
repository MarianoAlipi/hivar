from structures.function_variable import Variable, Function


class Scope:
    def __init__(self):
        self.__funcs = {}
        self.__vars = {}
        self.__scopes = {}
        self.__parent = None
        self.__attributes = []

    def funcs(self):
        return self.__funcs

    def vars(self):
        return self.__vars

    def scopes(self):
        return self.__scopes

    def parent(self):
        return self.__parent

    def set_parent(self, parent):
        self.__parent = parent

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
        self.__funcs[new_name] = Function(new_name, func_type, [])
        return self.__funcs[new_name]

    def add_var(self, new_name, var_type=None, is_const=False):
        if new_name in self.vars() and not is_const:
            raise Exception(
                f'Variable "{new_name}" is already declared in this scope')
        self.__vars[new_name] = Variable(new_name, var_type)

    def get_var_from_id(self, var_id):
        if var_id in self.vars():
            return self.vars()[var_id]
        else:
            parent_scope = self.parent()
            if parent_scope:
                var = parent_scope.get_var_from_id(var_id)
                if var:
                    return var
                return None
            else:
                raise Exception(
                    f'Can not find variable "{var_id}"')

    def get_func_from_id(self, func_id):
        if func_id in self.funcs():
            return self.funcs()[func_id]
        else:
            parent_scope = self.parent()
            if parent_scope:
                func = parent_scope.get_func_from_id(func_id)
                if func:
                    return func
                return None
            else:
                raise Exception(
                    f'Can not find function "{func}"')

    def add_attribute(self, attr):
        self.__attributes.append(attr)

    def set_vars_as_attrs(self):
        for var in self.vars():
            self.add_attribute(var)
