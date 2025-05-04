def simple_one(n):
    return any(i + i < 22 for i in range(n + n))


def simple_two(n):
    return all(i + i < 22 for i in range(n + n))


def nested(n):
    return all(any(i + i < 22 for i in range(n + j)) for j in range(n + n))


def disjunctive_normal_form(n):
    return any((i > 0 or i + i < 34) and (i < n or i + i > n) for i in range(n + n))


def negation(n):
    return any(not (i + i < 22 or i > 3) for i in range(n + n))


def equality(n):
    return any(i + i == 22 and i < 33 for i in range(n + n))


def inequality(n):
    return any(i + i != 22 or i != 3 for i in range(n + n))


def vars_on_both_sides(n):
    return any(i + i < 4 + i and 3 * i > 2 * n for i in range(n + n))


def main():
    pass


if __name__ == "__main__":
    main()
