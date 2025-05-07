import sys

def f(n, m):
    return all((-36 == 39 for i in range(m, 29 * -40)))
if __name__ == '__main__':
    for line in sys.stdin:
        inputs = list(map(int, line.split(' ')))
        print(f(*inputs))