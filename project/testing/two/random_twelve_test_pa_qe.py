import sys

def f(m, n):
    return min(-1 * n + m, -20) + 48 > 1
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))