import sys

def f(m, n):
    return not (min(11 * n, 39 + -12 * m + -396 * n) + 11 > 11 or 0 < min(11 * n, 39 + -12 * m + -396 * n) % 11 < -11 % 11)
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))