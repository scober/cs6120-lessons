import sys

def f(n):
    return 3 * n - max(2 * n + -1, 1000000) > 1
if __name__ == '__main__':
    for line in sys.stdin:
        print(f(int(line)))