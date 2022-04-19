"""This module provides some re-implementation of itertools functions for iterables"""


class Zip:
    """Implements connecting elements of different iterables in groups"""

    def __init__(self, *iterables):
        self.generated = self.generator(*iterables)

    def generator(self, *iterables):
        length = min([len(iterable) for iterable in iterables])
        for i in range(length):
            result = [iterable[i] for iterable in iterables]
            yield result

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.generated)


class Chain:
    """Implements chaining iterables to one iterable"""

    def __init__(self, *iterables):
        self.chained = (i for iterable in iterables for i in iterable)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.chained)


class Product:
    """Implements cartesian product of iterables"""

    def __init__(self, *iterables):
        self.generated=self.generator(*iterables)
        self.current = 0

    def __iter__(self):
        return self

    def generator(self, *iterables):
        def inner(left, cur):
            if left == len(iterables):
                yield tuple(cur)
                return
            for i in iterables[left]:
                yield from inner(left + 1, cur + [i])  #Алгоритм поиска в глубину
        yield from inner(0, [])

    def __next__(self):
        return next(self.generated)


class FileManager:
    """Context manager for files"""

    def __init__(self, filename, mode):
        self.file = open(filename, mode, encoding="utf-8")

    def __enter__(self):
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def write(self, text):
        """writes text into a file, be careful with open mode"""
        self.file.write(text)

    def read(self):
        """reads every char from file, be careful with open mode"""
        return self.file.read()

    def readline(self):
        """reads line from the file, be careful with open mode"""
        return self.file.readline()

    def readlines(self):
        """reads all lines from the file, be careful with open mode"""
        return self.file.readlines()
