import pytest
from random import randint
from math import factorial as math_factorial
from python.algorithms_structures.algorithms.factorial import factorial as my_factorial


@pytest.mark.parametrize("test_input", [randint(0, 100) for i in range(20)])
def test_valid_factorial(test_input):
    assert my_factorial(test_input) == math_factorial(test_input)


@pytest.mark.parametrize("test_input", [12.5, "123", [1, 2], None])
def test_invalid_factorial(test_input):
    with pytest.raises(TypeError):
        my_factorial(test_input)


def test_negative_input():
    with pytest.raises(ValueError):
        my_factorial(-10)