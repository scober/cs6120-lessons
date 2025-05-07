import sys


def f(n):
    return all((34 < -25 for i in range(-5 + 5 - -33, 6 * (-30 * -13))))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
