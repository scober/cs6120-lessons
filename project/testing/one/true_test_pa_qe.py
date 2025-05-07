import sys

def f(n):
    return min(1000000, 3 * n) - (2 * n + -1) > 1 or (2 * n + -1) % 1 < min(1000000, 3 * n) % 1
if __name__ == '__main__':
    for line in sys.stdin:
        print(f(int(line)))