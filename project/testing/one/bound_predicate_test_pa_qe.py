import sys

def f(n):
    return not min(1 + -27 * n, n) + 28 > 1
if __name__ == '__main__':
    for line in sys.stdin:
        print(f(int(line)))