"""This module implements graph"""
from my_linked_list import LinkedList


class Graph:
    """Graph implementation class"""
    def __init__(self, vertex):
        self.main_vertex = Graph.Vertex(vertex, None, None)

    def insert(self, vertex, *connections):
        """inserts vertex with connections into graph"""
        current = self.main_vertex
        while current.next_vertex is not None:
            current = current.next_vertex
        filtered_connections = LinkedList(vertex)
        for connection in connections:
            if self.lookup(connection):
                filtered_connections.prepend(self.lookup(connection))
        current.next_vertex = Graph.Vertex(vertex, None,
                                           filtered_connections)

    def delete(self, vertex):
        """delete`s vertex and it's connections from graph"""
        previous = None
        node = self.main_vertex
        while node:
            if node.info == vertex:
                if node == self.main_vertex:
                    self.main_vertex = self.main_vertex.next_vertex
                previous.next_vertex = node.next_vertex
                for connection in node.connections:
                    connection.connections.delete(connection.connections.lookup(node))
                node = None
                return
            previous = node
            node = node.next_vertex

    def lookup(self, vertex):
        """returns node by given value"""
        current = self.main_vertex
        while current is not None:
            if current.info == vertex:
                return current
            current = current.next_vertex
        return current

    class Vertex:
        """Class for graph`s vertexes based """
        def __init__(self, vertex, next_vertex, filtered_connections):
            self.info = vertex
            self.next_vertex = next_vertex
            self.connections = LinkedList(self)
            if filtered_connections:
                for connection in filtered_connections:
                    if isinstance(connection, Graph.Vertex):
                        self.establish_connection(connection)

        def establish_connection(self, another):
            """establishes connection between to vertexes"""
            if another not in self.connections:
                self.connections.prepend(another)
            if self not in another.connections:
                another.connections.prepend(self)
