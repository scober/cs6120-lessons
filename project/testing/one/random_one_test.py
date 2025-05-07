import sys


def f(n):
    return all((-35 != 16 for i in range(n - (41 + 7 * (-24 * -36)) - 22 + 19, 50)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
