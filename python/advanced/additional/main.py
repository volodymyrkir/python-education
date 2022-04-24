"""This module is used in testing iterators.py module"""
from generator import gen_fib
from log_decorator import log
from iterators import Zip, Chain, Product, FileManager


@log
def main():
    g = gen_fib(10)
    for i in g:
        print(i, end=" ")
    l = [1, 2, 3, 4, 5]
    s = "abcd"
    t = (1, 2, 3)
    for z in Zip(l, s, t):
        print(z)
    for i in Chain([1, 2, 3], [4, 5], "678910str"):
        print(i)
    for i in Product([1, 2, 3], (2, 3)):
        print(i)
    with FileManager("new.txt", "w") as file:
        file.write("Smth")


main()
