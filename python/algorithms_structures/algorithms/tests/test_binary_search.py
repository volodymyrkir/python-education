import pytest
from random import sample, choice
from python.algorithms_structures.algorithms.binary_search import BinarySearch


@pytest.fixture()
def binary_search_object():
    return BinarySearch()


@pytest.mark.parametrize("test_input", [[sample(range(-10, 100), 10)] for i in range(10)])
def test_search_default(binary_search_object, test_input):
    random_item = choice(test_input)
    sorted_input = sorted(test_input)
    expected = sorted_input.index(random_item)
    assert binary_search_object.binary_search(test_input, random_item) == expected


@pytest.mark.parametrize("test_input", [sample(range(9), 9) for i in range(10)])  # string of integers
def test_search_string(binary_search_object, test_input):
    to_string = "".join(map(str, sorted(test_input)))
    sorted_input=sorted(to_string)
    random_item = choice(sorted_input)
    expected = to_string.index(random_item)
    assert binary_search_object.binary_search(to_string, random_item) == expected


@pytest.mark.parametrize("test_input, element, expected", [("abcdefgh","h", 7), ("hgfedcab","h", 0),("python","h",0)])
def test_search_sentence(binary_search_object, test_input, element, expected):
    random_item = choice(test_input)
    sorted_input = sorted(test_input)
    expected = sorted_input.index(random_item)
    assert binary_search_object.binary_search(test_input, random_item) == expected


@pytest.mark.parametrize("test_input,element", [(123,3), (123.5,5), (None, 0)])
def test_search_invalid(binary_search_object,test_input, element):
    with pytest.raises(TypeError):
        binary_search_object.binary_search(test_input, None)
