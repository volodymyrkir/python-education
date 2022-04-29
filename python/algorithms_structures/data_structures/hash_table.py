"""This module implements hash tables based on linked lists"""
from my_linked_list import LinkedList


class HashTable:
    """Hash table based on linked list (O(n))"""
    def __init__(self):
        self.head = None

    def hash_func(self, info: str):
        """Getting hash from key"""
        if isinstance(info, int):
            return info % 30
        sum_str = 0
        for i in info:
            sum_str += ord(i)  # unicode
        return sum_str % 30

    def insert(self, key, value):
        """inserts new node with hash and value"""
        key_hash = self.hash_func(key)
        if self.head is None:
            self.head = HashTable.HashNode(key_hash, value, None)
        else:
            previous = None
            current = self.head
            while current is not None:
                if current.hash == key_hash:
                    current.collision_node.append(HashTable.HashNode(key_hash, value, None))
                    return
                previous = current
                current = current.next_node
            previous.next_node = HashTable.HashNode(key_hash,value, None)

    def lookup(self, key):
        """Returns value by key"""
        hash_key = self.hash_func(key)
        current = self.head
        while current is not None:
            if current.hash == hash_key:
                if current.collision_node.get_size() == 1:
                    return current.collision_node[0].value
                else:
                    return current.collision_node
            current = current.next_node

    def delete(self, key):
        """Deletes element from hash table"""
        hash_key = self.hash_func(key)
        previous = None
        current = self.head
        while current is not None:
            if current.hash == hash_key:
                previous.next_node = current.next_node
                del current
                return
            else:
                previous = current
                current = current.next_node

    class HashNode:
        """serves as hash table node"""
        def __init__(self, hash, value, next_node):
            self.hash = hash
            self.value = value
            self.next_node = next_node
            self.collision_node = LinkedList(self)
