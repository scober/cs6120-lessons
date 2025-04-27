def eliminatable(n):
    return any(n % i == 0 for i in range(n))


def non_eliminatable(n):
    return any(n * n % i == 0 for i in range(n))


def main():
    print(eliminatable(6))
    print(non_eliminatable(6))


if __name__ == "__main__":
    main()
