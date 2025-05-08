import sys

def f(n):
    return not (0 > 589 * n + 859 and min(46112, 46112) - max(-1, -1) > 1)
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))