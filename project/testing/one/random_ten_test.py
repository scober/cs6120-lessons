import sys


def f(n):
    return all((-31 * (19 * n) < 20 * 43 for i in range(-13 + -45 * (-25 * 41))))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
