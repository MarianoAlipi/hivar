# script that handles index stacks, one for matrix and one for arrays
# we use stacks so that we can access different indexes in the same statement
# they were originally handled by the Virtual Machine, but we had several import problems so we moved them to their own file
# no logic, only getters, the stack is handled by its own methods
from structures.stack import Stack

__matrix_index_stack = Stack()
__array_index_stack = Stack()


def matrix_index():
    return __matrix_index_stack


def array_index():
    return __array_index_stack
