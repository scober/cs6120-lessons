import sys

def f(n):
    return 22 < 2 * (2 * n)
if __name__ == '__main__':
    for line in sys.stdin:
        print(f(int(line)))