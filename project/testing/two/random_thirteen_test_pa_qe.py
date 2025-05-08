import sys

def f(m, n):
    return not (min(-396 * n + -12 * m + 39, 11 * n) + 11 > 11 or min(-396 * n + -12 * m + 39, 11 * n) % 11 < -11 % 11)
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))