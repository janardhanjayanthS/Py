
numbers = (1, 5, 6, 7, 8, 3, 55)

num_iterator = iter(numbers)
# print(num_iterator)

# print(num_iterator.__iter__())

# print(next(num_iterator))


class SquareIterator:
    def __init__(self, sequence):
        self._sequence = sequence
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._sequence):
            square = self._sequence[self._index] ** 2
            self._index += 1
            return square
        else:
            raise StopIteration


sq_seq = SquareIterator([1, 5, 9, 21])
# print(sq_seq.__iter__())

# print(sq_seq.__next__())


# Generators


def gen(n):
    yield n
    yield n + 1


# for n in gen(5):
#     print(n)


def fibonacci(n):
    a, b = 0, 1
    while n:
        yield b
        a, b = b, a + b
        # n -= 1


# for n in fibonacci(10):
#     print(n)


def gen1():
    yield {'abcd': 'content'}

print(gen1())
print(gen1().__dir__)
# print(next(gen1()))
