import sys


def f(n):
    return all((not not not (-10 - (i + 41 * n) + n == 15 * (34 * i) + 32 and n == i) for i in range(-5 * -46, n - 41)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
