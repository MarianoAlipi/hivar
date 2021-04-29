def valid(self):
    if len(self.stack()) <= 0:
        raise Exception(
            "stack is empty")
    return True


def is_empty(self):
    if len(self.stack()) == 0:
        return True
    return False


class Stack:

    def __init__(self):
        self.__stack = []

    def stack(self):
        return self.__stack

    def push(self, val):
        self.__stack.append(val)

    def pop(self):
        if valid(self):
            element = self.__stack.pop()
            if element == '+' or element == '-' or element == '*' or element == '/':
                print(element)
            return element

    def top(self):
        if is_empty(self):
            return None
        return self.__stack[-1]
