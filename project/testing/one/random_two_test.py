import sys


def f(n):
    return all((n >= 23 for i in range(-34)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
