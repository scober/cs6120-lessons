import sys


def f(n):
    return any(i + i != 22 or i != 3 for i in range(n + n))


if __name__ == "__main__":
    for line in sys.stdin:
        print(f(int(line)))
