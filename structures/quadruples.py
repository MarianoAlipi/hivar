class Quad:

    def __init__(self, operator, left_op, right_op, result):
        self.__operator = operator
        self.__left_op = left_op
        self.__right_op = right_op
        self.__res = result

    def operator(self):
        return self.__operator

    def left_op(self):
        return self.__left_op

    def right_op(self):
        return self.__right_op

    def result(self):
        return self.__res

    def set_res(self, new_res):
        self.__res = new_res

    def unpack(self):
        return self.__operator, self.__left_op, self.__right_op, self.__res

    def print(self):
        print(f'{self.operator()} {self.left_op()} {self.right_op()} {self.result()}')
