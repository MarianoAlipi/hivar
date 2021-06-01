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
        # a scope can have other scopes, ex: global has class scopes, class scope have method scopes
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
        # creates new function with empty params, params will be added later
        self.__funcs[new_name] = Function(new_name, func_type, [])
        return self.__funcs[new_name]

    def add_var(self, new_name, var_type=None, is_const=False):
        if new_name in self.vars() and not is_const:
            raise Exception(
                f'Variable "{new_name}" is already declared in this scope')
        self.__vars[new_name] = Variable(new_name, var_type)

    def add_obj_var(self, global_scope, new_name, var_type):
        if new_name in self.vars():
            raise Exception(
                f'Variable "{new_name}" is already declared in this scope')
        # checks that the class actually exists
        if var_type not in global_scope.scopes():
            raise Exception(
                f'class "{var_type}" not found in global scope')
        class_scope = global_scope.scopes()[var_type]
        attributes = class_scope.attributes()
        var_attrs = {}
        var_attrs['type'] = var_type
        for attr in attributes:
            var_attrs[attr] = Variable(
                attr, class_scope.vars()[attr].var_type())
        # sets the attributes as the content in the var.
        self.__vars[new_name] = var_attrs

    def get_var_from_id(self, var_id):
        if var_id in self.vars():
            return self.vars()[var_id]
        elif type(var_id) == tuple:  # objects are tuples of (instance, attribute)
            object_var = self.get_var_from_id(var_id[0])
            return object_var[var_id[1]]
        else:
            # checks for vars in higher scopes in case they didnt find it
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
            # checks for func in higher scopes in case they didnt find it
            parent_scope = self.parent()
            if parent_scope:
                func = parent_scope.get_func_from_id(func_id)
                if func:
                    return func
            else:
                # si no tiene parent scope, es porque ya esta en el global, busca en cada clase el método
                for scope in self.scopes():
                    if func_id in self.scopes()[scope].funcs():
                        return self.scopes()[scope].funcs()[func_id]
                breakpoint()
                raise Exception(
                    f'Can not find function "{func_id}"')

    def add_attribute(self, attr):
        self.__attributes.append(attr)

    def set_vars_as_attrs(self):
        for var in self.vars():
            self.add_attribute(var)
