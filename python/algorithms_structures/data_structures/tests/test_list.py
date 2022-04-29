import pytest
from random import randint
from python.algorithms_structures.data_structures.my_linked_list import LinkedList


@pytest.fixture()
def linked_list():
    return LinkedList(1)


@pytest.mark.parametrize("test_input", [randint(0,20) for i in range(20)])
def test_append(linked_list, test_input):
    linked_list.append(test_input)
    assert linked_list[1] == test_input


def test_append_toempty(linked_list):
    linked_list.delete(0)
    linked_list.append(1)
    assert linked_list[0] == 1


@pytest.mark.parametrize("test_input", [randint(0,20) for i in range(20)])
def test_prepend(linked_list,test_input):
    linked_list.prepend(test_input)
    assert linked_list[0] == test_input


def test_prepend_empty(linked_list):
    linked_list.delete(0)
    linked_list.prepend(10)
    assert linked_list.head.info == 10


def test_delete(linked_list):
    linked_list.delete(0)
    assert linked_list.head is None


@pytest.mark.parametrize("test_input", [randint(2,20) for i in range(20)])
def test_incorrect_get(linked_list,test_input):
    with pytest.raises(IndexError):
        linked_list[test_input]


def test_generator_list(linked_list):
    for i in range(2, 11):
        linked_list.append(i)
    assert [i for i in linked_list] == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def test_lookup(linked_list):
    linked_list.append(3)
    linked_list.append(2)
    linked_list.append(2)
    assert linked_list.lookup(2) == 2


@pytest.mark.parametrize("test_input", [randint(0,20) for i in range(20)])
def test_insert_head(linked_list, test_input):
    linked_list.insert(test_input, 0)
    assert linked_list.lookup(test_input) == 0


def test_insert_middle(linked_list):
    linked_list.append(2)
    linked_list.insert(10, 1)
    assert linked_list.lookup(2) == 2


def test_insert_tail(linked_list):
    linked_list.append(2)
    linked_list.insert(10, 2)
    assert linked_list.lookup(10) == 2


def test_insert_incorrect(linked_list):  # inserts in end
    linked_list.append(2)
    linked_list.insert(10, 5)
    assert linked_list.lookup(10) == 2


def test_insert_negative(linked_list):  # inserts in head
    with pytest.raises(IndexError):
        linked_list.append(2)
        linked_list.insert(10, -10)
        assert linked_list.lookup(10) == 0
