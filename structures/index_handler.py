from structures.stack import Stack

__matrix_index_stack = Stack()
__array_index_stack = Stack()


def matrix_index():
    return __matrix_index_stack


def array_index():
    return __array_index_stack
