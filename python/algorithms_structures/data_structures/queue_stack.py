"""This module implements queues and stacks"""
from my_linked_list import AbstractList


class Queue(AbstractList):  # FIFO
    """Queue class based on linked list"""
    def enqueue(self, info):
        """adds element to the end of queue"""
        self._append(info)

    def dequeue(self):
        """retrieves first element of queue"""
        if self.head is None:
            item = None
        else:
            item = self.head.info
            self._delete(0)
        return item

    def peek(self):
        """returns value of first element in queue"""
        if self.head:
            return self.head.info


class Stack(AbstractList):  # LIFO
    """Stack implementation based on linked list"""
    def push(self, info):
        """adds element to the start of stack"""
        self._prepend(info)

    def peek(self):
        """returns value of first element in the stack"""
        return self.head.info

    def pop(self):
        """returns first node of the stack"""
        value = self.head
        if value is not None:
            self._delete(0)
            return value.info
        return value
