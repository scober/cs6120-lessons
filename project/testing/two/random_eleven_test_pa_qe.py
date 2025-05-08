import sys

def f(m, n):
    return n + -28 + 17 < -35 or n + -28 + 17 > -35
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))