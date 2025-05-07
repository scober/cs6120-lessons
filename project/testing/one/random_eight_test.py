import sys


def f(n):
    return all((-26 <= -24 or -33 > -2 for i in range(9)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
