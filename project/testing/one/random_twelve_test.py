import sys


def f(n):
    return all((not i != 20 and n > n for i in range(34 * n)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
