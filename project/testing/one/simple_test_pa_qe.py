import sys

def f(n):
    return 3 * n - max(n, 2 * n + -1) > 1
if __name__ == '__main__':
    for line in sys.stdin:
        print(f(int(line)))