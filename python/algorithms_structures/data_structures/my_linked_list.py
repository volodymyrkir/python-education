"""This module contains linked list implementation and abstractlist as base for other collections"""
from abc import ABC


class AbstractList(ABC):
    """Base class for different collections"""
    class Node:
        """Node class for lists and other collections"""
        def __init__(self, info, next_node):
            self.info = info
            self.next_node = next_node

    def __init__(self, info):
        self.head = AbstractList.Node(info, None)
        self.tail = None

    def _prepend(self, info):
        """Adds element in the start of collection"""
        if self.tail is None:
            self.tail = self.head
        self.head = AbstractList.Node(info, self.head)

    def _append(self, info):
        """Adds element in the end of connection"""
        if self.head is None:
            self.head = AbstractList.Node(info, None)
        else:
            if self.tail is None:
                self.tail = AbstractList.Node(info, None)
                self.head.next_node = self.tail
            else:
                new_node = AbstractList.Node(info, None)
                self.tail.next_node = new_node
                self.tail = new_node

    def _delete(self, index):
        """Deletes element from collection"""
        if index < 0:
            raise IndexError
        previous = None
        current = self.head
        while index > 0:
            previous = current
            current = current.next_node
            if current is None:
                raise IndexError
            index -= 1
        if previous is None:
            self.head = self.head.next_node
        else:
            self.tail = previous
            previous.next_node = None
        del current

    def __getitem__(self, item):
        """implements [] operator to get element by index"""
        if item < 0:
            raise IndexError
        current = self.head
        while item > 0:
            if current is None:
                raise IndexError
            current = current.next_node
            item -= 1
        return current.info

    def __iter__(self):
        self.generator = self.list_generator()
        return self

    def list_generator(self):
        """Returns generator of collection"""
        current = self.head
        while current is not None:
            yield current.info
            current = current.next_node

    def __next__(self):
        return next(self.generator)


class LinkedList(AbstractList):
    """Basic linked list implementation"""
    def get_size(self):
        """returns size of linked list"""
        current = self.head
        counter =0
        while current is not None:
            counter+=1
            current=current.next_node
        return counter

    def prepend(self, info):
        """implements AbstractList`s method"""
        self._prepend(info)

    def append(self, info):
        """implements AbstractList`s method"""
        self._append(info)

    def lookup(self, item):
        """returns index of first occurrence of item"""
        current = self.head
        index = 0
        while current is not None:
            if current.info == item:
                return index
            index += 1
            current = current.next_node
        return None

    def insert(self, info, index):
        """Inserts element shifting other elements to the right side"""
        if index < 0:
            raise IndexError
        current = self.head
        previous = None
        while index > 0:
            if current is None:
                break
            previous = current
            current = current.next_node
            index -= 1
        if previous is None:  # if insert on 0 index
            self.prepend(info)
        elif current is None:  # if insert on last or more than last index
            self.append(info)
        else:
            new_node = LinkedList.Node(info, current)
            previous.next_node = new_node

    def delete(self, index):
        """implements AbstractList`s method"""
        self._delete(index)
