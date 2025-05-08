import sys


def f(n):
    return any((not n >= n or ((not -48 >= n and ((42 * (6 * (i + (18 - 19 * n))) == -4 or 2 < 27) or (i >= 28 - i and -36 == 16))) and 43 == 25 * (n - 42)) for i in range(-27, n)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
