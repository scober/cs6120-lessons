import sys


def f(m, n):
    return all((-17 == m for i in range(m)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
