import sys


def f(n, m):
    return all((-20 == 33 or -37 >= 5 for i in range(-27 * 25)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
