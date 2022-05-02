"""This module implements binary search class"""
from math import floor


class BinarySearch:
    """class, that encapsulates logic concerned to binary search"""
    def binary_search(self, iterable, element):
        """main method, that calls functions on the iterable"""
        sorted_iterable = self.__prepare_iterable(iterable)
        return self.__main_algorithm(sorted_iterable, element)

    def __prepare_iterable(self, iterable):
        """returns sorted iterable"""
        return sorted(iterable)

    def __main_algorithm(self, iterable, element):
        """finds index of element in SORTED iterable"""
        left_border = 0
        right_border = len(iterable) - 1
        while left_border <= right_border:
            middle_index = floor((left_border + right_border) / 2)
            if iterable[middle_index] < element:
                left_border = middle_index + 1
            elif iterable[middle_index] > element:
                right_border = middle_index - 1
            else:
                return middle_index
        return None  # if element not in iterable
