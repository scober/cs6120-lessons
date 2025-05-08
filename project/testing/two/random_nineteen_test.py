import sys


def f(m, n):
    return all((not (i <= 27 * n or not n >= -33 - -12) for i in range(-27, -46 * (n + -30))))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
