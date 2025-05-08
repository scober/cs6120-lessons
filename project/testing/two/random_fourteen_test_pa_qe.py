import sys

def f(m, n):
    return not (min(-1 * (-1 + -1 * m), -13600) - 425 * (-1 + m) > 425 or min(-1 * (-1 + -1 * m), -13600) % 425 < 425 * (-1 + m) % 425)
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))