def valid(self):
    if len(self.stack) <= 0:
        raise Exception(
            "stack is empty")
    return True


class Stack:

    def __init__(self):
        self.__stack = []

    def push(self, val):
        self.__stack.append(val)

    def pop(self):
        if valid(self):
            return self.__stack.pop()

    def top(self):
        if valid(self):
            return self.__stack[-1]