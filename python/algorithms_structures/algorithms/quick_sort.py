"""This module implements iterative(recursive) quicksort"""


class QuickSort:
    """Quick sort class that encapsulates all logic concerned to this sort"""
    def __get_length(self, iterable):
        """returns length of list"""
        if not isinstance(iterable, list):
            raise TypeError     # for in-place sorting
        return len(iterable)

    def quick_sort(self, iterable):
        """main method that calls other methods"""
        return self.__main_algorithm(iterable, 0, self.__get_length(iterable) - 1)

    def __main_algorithm(self, iterable, start, end):
        """main algorithm that uses Hoar partition based on iteration over list"""
        if end < 1:
            return None
        storage = [[start, end]]
        while len(storage) > 0:
            lower, higher = storage.pop()
            pivot = iterable[(lower + higher) // 2]
            i = lower - 1
            j = higher + 1
            i, j = self.__iterate_over_collection(iterable, i, j, pivot)
            if j > lower:
                storage.append([lower, j])
            j += 1
            if higher > j:
                storage.append([j, higher])

    def __iterate_over_collection(self, iterable, i, j, pivot):
        """iteration over list to swap elements"""
        while True:
            while True:  # may be wrong
                i += 1
                if iterable[i] >= pivot:
                    break
            while True:
                j -= 1
                if iterable[j] <= pivot:
                    break
            if i >= j:
                break
            iterable[i], iterable[j] = iterable[j], iterable[i]
        return i, j
