import sys

def f(l, m, n):
    return not min(m, -1 * (-1 * m)) + 1 > 1
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))