import sys

def f(n):
    return not -1 * n + 1 - max(n, -1) > 1
if __name__ == '__main__':
    for line in sys.stdin:
        print(f(int(line)))