def simple_one(n):
    return -2 - max(2 * (2 * n), 22) > 2 or -2 % 2 < max(2 * (2 * n), 22) % 2


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
        (min(n, -2, 0) - 2 * (2 * n) > 2 or min(n, -2, 0) % 2 < 2 * (2 * n) % 2)
        or (
            min(n, -2) - max(34, 2 * (2 * n)) > 2
            or min(n, -2) % 2 < max(34, 2 * (2 * n)) % 2
        )
    )


def negation(n):
    return min(4, -2, 21) - 2 * (2 * n) > 2 or min(4, -2, 21) % 2 < 2 * (2 * n) % 2


def equality(n):
    return 22 < 2 * (2 * n)


def inequality(n):
    return (
        (-2 - max(2 * (2 * n), 22) > 2 or -2 % 2 < max(2 * (2 * n), 22) % 2)
        or (min(22, -2) - 2 * (2 * n) > 2 or min(22, -2) % 2 < 2 * (2 * n) % 2)
    ) or (
        (-1 - max(3, 2 * n) > 1 or -1 % 1 < max(3, 2 * n) % 1)
        or (min(-1, 3) - 2 * n > 1 or min(-1, 3) % 1 < 2 * n % 1)
    )


def vars_on_both_sides(n):
    return (
        min(-3, 2 * n) - max(3 * (2 * n), 12) > 3
        or min(-3, 2 * n) % 3 < max(3 * (2 * n), 12) % 3
    )


def main():
    pass


if __name__ == "__main__":
    main()
