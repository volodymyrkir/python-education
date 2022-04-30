import pytest
from random import randint
from python.algorithms_structures.data_structures.queue_stack import Queue, Stack


@pytest.fixture()
def queue_default():
    return Queue(1)


@pytest.fixture()
def stack_default():
    return Stack(1)


def test_queue_init(queue_default):
    assert queue_default[0]


@pytest.mark.parametrize("test_input", [randint(0, 30) for i in range(10)])
def test_queue_enqueue(queue_default,test_input):
    queue_default.enqueue(test_input)
    assert queue_default[1] == test_input


@pytest.mark.parametrize("test_input", [randint(0, 10) for i in range(20)])
def test_queue_dequeue(queue_default,test_input):
    queue_default.dequeue()
    queue_default.enqueue(test_input)
    assert queue_default.dequeue() == test_input
    assert queue_default.dequeue() is None



def test_queue_peek(queue_default):
    assert queue_default.peek() == 1


def test_queue_peeknone(queue_default):
    queue_default.dequeue()
    assert queue_default.peek() is None


def test_stack_init(stack_default):
    assert stack_default[0] == 1


@pytest.mark.parametrize("test_input", [randint(-5, 20) for i in range(20)])
def test_stack_push(stack_default, test_input):
    stack_default.push(test_input)
    assert stack_default[0] == test_input


@pytest.mark.parametrize("test_input", [randint(-5, 20) for i in range(20)])
def test_stack_pop(stack_default,test_input):
    stack_default.push(test_input)
    assert stack_default.pop() == test_input


def test_stack_peek(stack_default):
    stack_default.push(2)
    assert stack_default.peek() == 2


def test_stack_iterator(stack_default):
    stack_default.push(2)
    stack_elems = [elem for elem in stack_default]
    assert stack_elems == [2, 1]
