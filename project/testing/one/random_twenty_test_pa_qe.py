import sys

def f(n):
    return not (min(-511 * (-1 * n), 511 * (-41 + n), -1 * (42 + 40 * n)) - max(-1 * (42 + 40 * n), 117019, -511 * (-1 * n)) > 511 or max(-1 * (42 + 40 * n), 117019, -511 * (-1 * n)) % 511 < min(-511 * (-1 * n), 511 * (-41 + n), -1 * (42 + 40 * n)) % 511)
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))