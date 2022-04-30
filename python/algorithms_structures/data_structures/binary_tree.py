"""This module implements binary tree"""


class BinaryTree:  # Not useful to inherit from linked_list, too many inappropriate methods
    """Binary tree class"""
    class BinaryNode:
        """Binary node with left and right branch"""
        def __init__(self, info):
            self.info = info
            self.right_node = None
            self.left_node = None

    def __init__(self, value):
        self.head = BinaryTree.BinaryNode(value)

    def insert(self, value):
        """inserts value in binary tree"""
        if isinstance(value, str):
            sum_str = 0
            for i in value:
                sum_str += ord(i)
            value = sum_str
        if self.head is None:
            self.head = BinaryTree.BinaryNode(value)
        previous = None
        current = self.head
        while current is not None:
            if current.info == value:
                return
            previous = current
            current, choice = (current.right_node, 1) if value > current.info else (current.left_node, 0)
        if choice:
            previous.right_node = BinaryTree.BinaryNode(value)
        else:
            previous.left_node = BinaryTree.BinaryNode(value)

    def look_up(self, value):
        """returns node with needed value"""
        current = self.head
        while current is not None:
            if current.info == value:
                return current
            current = current.right_node if value > current.info else current.left_node
        return current  # None

    def delete(self, value):
        """deletes value from tree"""
        if self.look_up(value) == self.head:  # if node is head
            if not self.head.left_node and not self.head.right_node:  # if no child
                self.head = None
            elif not self.head.right_node:  # if no bigger child
                self.head = self.head.left_node
            else:
                self.head = self.head.right_node
        else:
            if self.look_up(value):
                previous = None
                current = self.head
                while not current.info == value:
                    previous = current
                    current, right_branch = (current.right_node, True) if value > current.info else (current.left_node, False)
                node = None
                if not current.left_node and not current.right_node:  # if no child
                    node = None
                elif not current.right_node:  # if no bigger child
                    node = current.left_node
                else:
                    node = current.right_node
                if right_branch:
                    previous.right_node = node
                else:
                    previous.left_node = node
                del current
