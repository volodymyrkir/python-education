
def gen_fib(end: int):
    first, second = 0, 1
    while end > 0:
        yield first
        first, second = second, first + second
        end -= 1
