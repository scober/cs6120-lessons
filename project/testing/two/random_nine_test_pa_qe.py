import sys

def f(n, m):
    return not (-7 <= m + 101187 and 8 - (-1 * n + -62) > 1)
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))