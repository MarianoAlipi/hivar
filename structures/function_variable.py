

class Variable:
    def __init__(self, name, var_type):
        self.__name = name
        self.__type = var_type
        self.__value = None
        self.__dims = None

    def name(self):
        return self.__name

    def var_type(self):
        return self.__type

    def value(self):
        return self.__value

    def dims(self):
        return self.__dims

    def set_i(self, i):
        self.__dims = i

    def set_j(self, j):
        self.__dims = (self.dims(), j)

    def i(self):
        # we only call these when it's specified that a value has dims, so we raise exceptions when they dont have any
        dims = self.dims()
        if not dims:
            raise Exception(f'trying to access i for atomic var {self.__name}')
        elif type(dims) is tuple:
            return dims[0]
        else:
            return dims

    def j(self):
        # we only call these when it's specified that a value has dims, so we raise exceptions when they dont have any
        dims = self.dims()
        if not dims:
            raise Exception(f'trying to access j for atomic var {self.__name}')
        elif type(dims) is tuple:
            return dims[1]
        else:
            raise Exception(f'trying to access j for array var {self.__name}')

    def get_size(self):
        # size refers to the amount of memory spaces needed
        dims = self.dims()
        if not dims:
            return 1
        elif type(dims) is tuple:
            # rows * cols
            return dims[0] * dims[1]
        else:
            return dims


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
