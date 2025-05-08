import sys


def f(n):
    return all(0 >= 1 + -2 * i + -4 * n for i in range(n))


if __name__ == "__main__":
    for line in sys.stdin:
        print(f(int(line)))
