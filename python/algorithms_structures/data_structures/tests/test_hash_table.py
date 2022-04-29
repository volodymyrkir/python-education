import pytest
from random import randint
from python.algorithms_structures.data_structures.hash_table import HashTable


@pytest.fixture()
def default_hash_table():
    h = HashTable()
    h.insert("123", [1, 2, 3])
    return h


def test_hash_init(default_hash_table):
    assert isinstance(default_hash_table.head, HashTable.HashNode)


@pytest.mark.parametrize("test_input,expected", [("111", [1,1,1]),("234", [2,3,4]),("345", [3,4,5])])
def test_hash_insert(default_hash_table,test_input,expected):    # +lookup
    default_hash_table.insert(test_input,expected)
    assert default_hash_table.lookup(test_input) == expected


def test_hash_delete(default_hash_table):
    default_hash_table.insert("234", [2, 3, 4])
    default_hash_table.delete("234")
    assert default_hash_table.lookup("234") is None
    assert default_hash_table.lookup("123") == [1, 2, 3]


def test_hash_collision(default_hash_table):
    default_hash_table.insert("234", (1, [2]))
    default_hash_table.insert("234", (2, [3]))
    assert default_hash_table.lookup("234")[1].value == (2, [3])
