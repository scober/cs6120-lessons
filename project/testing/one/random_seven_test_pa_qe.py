import sys

def f(n):
    return not (0 == 4535 + -1 * n and min(-39, -39) - max(-1, -1) > 1)
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))