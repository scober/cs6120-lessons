import sys

def f(n, m):
    return not -1160 - (m + -1) > 1
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))