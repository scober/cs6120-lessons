import sys

def f(m, n):
    return not (-17 < m and m + 1 > 1 or (-17 > m and m + 1 > 1))
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))