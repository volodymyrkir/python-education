import pytest
from random import randint
from copy import copy
from python.algorithms_structures.algorithms.quick_sort import QuickSort


@pytest.fixture()
def quick_sort_object():
    return QuickSort()


@pytest.mark.parametrize("test_input", [[randint(-100,100) for i in range(randint(0, 10))] for i in range(10)])
def test_quick_sort(test_input, quick_sort_object):
    copy_input = copy(test_input)
    quick_sort_object.quick_sort(test_input)
    assert test_input == sorted(copy_input)


@pytest.mark.parametrize("test_input", [(1,2,3), "Str", 1, 1.5, {}])
def test_sort_type(quick_sort_object,test_input):
    with pytest.raises(TypeError):
        quick_sort_object.quick_sort(test_input)


@pytest.mark.parametrize("test_input", [[], [1,2], [1]])
def test_sort_bottlenecks(quick_sort_object, test_input):
    copy_input = copy(test_input)
    quick_sort_object.quick_sort(test_input)
    assert test_input == sorted(copy_input)
