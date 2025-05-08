import sys


def f(n):
    return all(n == 1 or n == 1 or 1 != n for i in range(0, n))


if __name__ == "__main__":
    for line in sys.stdin:
        print(f(int(line)))
