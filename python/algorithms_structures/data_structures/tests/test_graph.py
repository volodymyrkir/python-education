import pytest
from random import randint
from python.algorithms_structures.data_structures.graph import Graph


@pytest.fixture()
def default_graph():
    return Graph(1)


def test_graph_init(default_graph):
    assert default_graph.main_vertex.info == 1


@pytest.mark.parametrize("test_input", [randint(0,10) for i in range(10)])
def test_graph_insert(default_graph,test_input):
    default_graph.insert(test_input,1)
    assert default_graph.main_vertex.connections[0].info == test_input


@pytest.mark.parametrize("test_input", [(2, 3), (3, 3), (4,5), (5,2), (7,2)])
def test_incorrect_insert(default_graph,test_input):
    default_graph.insert(*test_input)
    assert default_graph.main_vertex.next_vertex.connections[0].info == test_input[0]  # No connections except 2


@pytest.mark.parametrize("test_input", [randint(0, 10) for i in range(20)])
def test_graph_lookup(default_graph,test_input):
    default_graph.insert(test_input)
    assert default_graph.lookup(test_input).info == test_input


def test_graph_delete(default_graph):
    default_graph.insert(2,1)
    default_graph.delete(2)
    assert default_graph.lookup(2) is None
