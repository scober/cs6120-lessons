import sys


def f(n):
    return all((not n == 37 and ((-27 * 47 == 17 - (n - n + 10 * (i + i) - (n + 13)) or not (n != n and (not ((-49 != i + -26 - i or (n <= i and (not -49 <= i))) or not i >= i)))) and 0 >= -32 * (n - i)) for i in range(n)))


if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))
