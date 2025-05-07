import sys


def f(n):
    return all((n - 47 != -34 * (12 * -11) for i in range(-39)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
