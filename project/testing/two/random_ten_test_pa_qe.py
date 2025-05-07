import sys

def f(n, m):
    return all((-3 >= -9 - -40 * -36 for i in range(23)))
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))