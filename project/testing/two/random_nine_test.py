import sys


def f(n, m):
    return all((-7 > m - (-24 + (-49 * (48 * 43) - 27)) for i in range(-26 - 35 - n, 8)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
