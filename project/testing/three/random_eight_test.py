import sys


def f(l, m, n):
    return all((43 >= n + n for i in range(-1 * 33 + m)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
