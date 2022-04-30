import pytest
from random import randint
from python.algorithms_structures.data_structures.binary_tree import BinaryTree


@pytest.fixture()
def default_tree():
    return BinaryTree(10)


def test_tree_init(default_tree):
    assert default_tree.look_up(10).info == 10


@pytest.mark.parametrize("test_input", [randint(0, 100) for i in range(20)])
def test_tree_insert(default_tree, test_input):
    default_tree.insert(test_input)
    assert default_tree.look_up(test_input) is not None


@pytest.mark.parametrize("test_input", [randint(0, 100) for i in range(20)])
def test_tree_delete(default_tree, test_input):
    default_tree.insert(test_input)
    default_tree.delete(10)
    if default_tree.head:
        assert default_tree.head.info == test_input
    else:
        assert default_tree.head is None
