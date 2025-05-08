import sys

def f(n):
    return not (0 < n + -38 and min(-46, -46) - max(-34, -34) > 1 or (0 > n + -38 and min(-46, -46) - max(-34, -34) > 1))
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))