"""This module is supposed to do the things,
that can be done in one line, in more than three lines"""


class Calculator:
    """This class implements several arithmetical operations."""
    def __init__(self, first, second):
        """initialize the calculator with 2 of it's operands"""
        self.first = first
        self.second = second

    def add(self):
        """Returns sum of arguments"""
        return self.first+self.second

    def subtract(self):
        """Returns subtraction of arguments"""
        return self.first-self.second

    def multiply(self):
        """Returns production of arguments"""
        return self.first*self.second

    def divide(self):
        """Returns division of arguments, handling zero division as 0"""
        try:
            res = self.first / self.second
        except ZeroDivisionError:
            return 0
        else:
            return res
