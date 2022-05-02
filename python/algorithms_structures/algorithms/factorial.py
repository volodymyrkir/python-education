"""This module implements recursive factorial evaluation"""


def factorial(integer: int, answer=1):
    """Recursive evaluation of factorial"""
    if not isinstance(integer, int):
        raise TypeError
    if integer<0:
        raise ValueError
    if integer <= 1:
        return answer
    return factorial(integer-1, answer*integer)
