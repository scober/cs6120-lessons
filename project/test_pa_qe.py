def simple_one(n):
    return -2 - max(22, 2 * (2 * n)) > 2 or -2 % 2 < max(22, 2 * (2 * n)) % 2


def simple_two(n):
    return not (min(-2, 21) - 2 * (2 * n) > 2 or min(-2, 21) % 2 < 2 * (2 * n) % 2)


def nested(n):
    return all(
        (
            -2 - max(22, 2 * (n + j)) > 2 or -2 % 2 < max(22, 2 * (n + j)) % 2
            for j in range(n + n)
        )
    )


def disjunctive_normal_form(n):
    return (
        (min(-1, 0) - max(2 * n, n) > 1 or min(-1, 0) % 1 < max(2 * n, n) % 1)
        or (
            -2 - max(2 * (2 * n), 2 * n, 34) > 2
            or -2 % 2 < max(2 * (2 * n), 2 * n, 34) % 2
        )
    ) or (
        (min(0, n, -2) - 2 * (2 * n) > 2 or min(0, n, -2) % 2 < 2 * (2 * n) % 2)
        or (
            min(-2, n) - max(2 * (2 * n), 34) > 2
            or min(-2, n) % 2 < max(2 * (2 * n), 34) % 2
        )
    )


def negation(n):
    return min(-2, 21, 4) - 2 * (2 * n) > 2 or min(-2, 21, 4) % 2 < 2 * (2 * n) % 2


def equality(n):
    return 22 > -2 and 22 < 2 * (2 * n) and (22 < 66)


def inequality(n):
    return (
        (-2 - max(2 * (2 * n), 22) > 2 or -2 % 2 < max(2 * (2 * n), 22) % 2)
        or (min(22, -2) - 2 * (2 * n) > 2 or min(22, -2) % 2 < 2 * (2 * n) % 2)
    ) or (
        (-1 - max(2 * n, 3) > 1 or -1 % 1 < max(2 * n, 3) % 1)
        or (min(-1, 3) - 2 * n > 1 or min(-1, 3) % 1 < 2 * n % 1)
    )


def vars_on_both_sides(n):
    return (
        min(2 * n, -3) - max(12, 3 * (2 * n)) > 3
        or min(2 * n, -3) % 3 < max(12, 3 * (2 * n)) % 3
    )


def main():
    pass


if __name__ == "__main__":
    main()
