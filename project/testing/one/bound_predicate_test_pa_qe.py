import sys

def f(n):
    return not min(-27 * n + 1, n) + 28 > 1
if __name__ == '__main__':
    for line in sys.stdin:
        print(f(int(line)))