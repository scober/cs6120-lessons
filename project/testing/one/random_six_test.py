import sys


def f(n):
    return all((25 <= -31 for i in range(36 * (35 - 48) + 49)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
