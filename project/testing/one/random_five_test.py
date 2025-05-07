import sys


def f(n):
    return any((-15 * -26 < -26 for i in range(44)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
