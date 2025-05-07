import sys


def f(n):
    return any(i > 1000000 for i in range(2 * n, 3 * n))


if __name__ == "__main__":
    for line in sys.stdin:
        print(f(int(line)))
