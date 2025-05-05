def simple_one(n):
    return any(
        (
            2 * i >= 2 * (0 + 0)
            and 2 * i < 2 * (0 + 2 * n)
            and (
                2 * i >= 1 * (0 + 0)
                and 2 * i < 1 * (0 + 4 * n + 0)
                and (
                    2 * i >= 1 * (0 + 0)
                    and 2 * i < 1 * (0 + 4 * n + 0)
                    and (
                        2 * i >= 1 * (0 + 0)
                        and 2 * i < 1 * (0 + 4 * n + 0)
                        and (2 * i < 1 * (0 + 22))
                    )
                )
            )
            for i in range(n + n)
        )
    )


def simple_two(n):
    return not any(
        (
            2 * i >= 2 * (0 + 0)
            and 2 * i < 2 * (0 + 2 * n)
            and (
                2 * i >= 1 * (0 + 0)
                and 2 * i < 1 * (0 + 4 * n + 0)
                and (
                    2 * i >= 1 * (0 + 0)
                    and 2 * i < 1 * (0 + 4 * n + 0)
                    and (
                        2 * i >= 1 * (0 + 0)
                        and 2 * i < 1 * (0 + 4 * n + 0)
                        and (2 * i >= 1 * (0 + 22))
                    )
                )
            )
            for i in range(n + n)
        )
    )


def nested(n):
    return all(
        (
            any(
                (
                    2 * i >= 2 * (0 + 0)
                    and 2 * i < 2 * (0 + 1 * j + 1 * n)
                    and (
                        2 * i >= 1 * (0 + 0)
                        and 2 * i < 1 * (0 + 2 * j + 2 * n + 0)
                        and (
                            2 * i >= 1 * (0 + 0)
                            and 2 * i < 1 * (0 + 2 * j + 2 * n + 0)
                            and (
                                2 * i >= 1 * (0 + 0)
                                and 2 * i < 1 * (0 + 2 * j + 2 * n + 0)
                                and (2 * i < 1 * (0 + 22))
                            )
                        )
                    )
                    for i in range(n + j)
                )
            )
            for j in range(n + n)
        )
    )


def disjunctive_normal_form(n):
    return (
        any(
            (
                1 * i >= 1 * (0 + 0)
                and 1 * i < 1 * (0 + 2 * n)
                and (
                    1 * i >= 1 * (0 + 0)
                    and 1 * i < 1 * (0 + 2 * n + 0)
                    and (1 * i > 1 * (0 + 0) and 1 * i < 1 * (0 + 1 * n + 0))
                )
                for i in range(n + n)
            )
        )
        or any(
            (
                2 * i >= 2 * (0 + 0)
                and 2 * i < 2 * (0 + 2 * n)
                and (
                    2 * i >= 1 * (0 + 0)
                    and 2 * i < 1 * (0 + 4 * n + 0)
                    and (2 * i < 1 * (0 + 34) and 2 * i < 1 * (0 + 2 * n + 0))
                )
                for i in range(n + n)
            )
        )
    ) or (
        any(
            (
                2 * i >= 2 * (0 + 0)
                and 2 * i < 2 * (0 + 2 * n)
                and (
                    2 * i >= 1 * (0 + 0)
                    and 2 * i < 1 * (0 + 4 * n + 0)
                    and (2 * i > 1 * (0 + 0) and 2 * i > 1 * (0 + 1 * n + 0))
                )
                for i in range(n + n)
            )
        )
        or any(
            (
                2 * i >= 2 * (0 + 0)
                and 2 * i < 2 * (0 + 2 * n)
                and (
                    2 * i >= 1 * (0 + 0)
                    and 2 * i < 1 * (0 + 4 * n + 0)
                    and (2 * i < 1 * (0 + 34) and 2 * i > 1 * (0 + 1 * n + 0))
                )
                for i in range(n + n)
            )
        )
    )


def negation(n):
    return any(
        (
            2 * i >= 2 * (0 + 0)
            and 2 * i < 2 * (0 + 2 * n)
            and (
                2 * i >= 1 * (0 + 0)
                and 2 * i < 1 * (0 + 4 * n + 0)
                and (
                    2 * i >= 1 * (0 + 0)
                    and 2 * i < 1 * (0 + 4 * n + 0)
                    and (
                        2 * i >= 1 * (0 + 0)
                        and 2 * i < 1 * (0 + 4 * n + 0)
                        and (2 * i >= 1 * (0 + 22) and 2 * i <= 1 * (0 + 6))
                    )
                )
            )
            for i in range(n + n)
        )
    )


def equality(n):
    return (
        1 * (0 + 22) >= 2 * (0 + 0)
        and 1 * (0 + 22) < 2 * (0 + 2 * n)
        and (True and 1 * (0 + 22) < 2 * (0 + 33))
    )


def inequality(n):
    return (
        any(
            (
                2 * i >= 2 * (0 + 0)
                and 2 * i < 2 * (0 + 2 * n)
                and (
                    2 * i >= 1 * (0 + 0)
                    and 2 * i < 1 * (0 + 4 * n + 0)
                    and (2 * i < 1 * (0 + 22))
                )
                for i in range(n + n)
            )
        )
        or any(
            (
                2 * i >= 2 * (0 + 0)
                and 2 * i < 2 * (0 + 2 * n)
                and (
                    2 * i >= 1 * (0 + 0)
                    and 2 * i < 1 * (0 + 4 * n + 0)
                    and (2 * i > 1 * (0 + 22))
                )
                for i in range(n + n)
            )
        )
    ) or (
        any(
            (
                1 * i >= 1 * (0 + 0)
                and 1 * i < 1 * (0 + 2 * n)
                and (
                    1 * i >= 1 * (0 + 0)
                    and 1 * i < 1 * (0 + 2 * n + 0)
                    and (1 * i < 1 * (0 + 3))
                )
                for i in range(n + n)
            )
        )
        or any(
            (
                1 * i >= 1 * (0 + 0)
                and 1 * i < 1 * (0 + 2 * n)
                and (
                    1 * i >= 1 * (0 + 0)
                    and 1 * i < 1 * (0 + 2 * n + 0)
                    and (1 * i > 1 * (0 + 3))
                )
                for i in range(n + n)
            )
        )
    )


def vars_on_both_sides(n):
    return any(
        (
            3 * i >= 3 * (0 + 0)
            and 3 * i < 3 * (0 + 2 * n)
            and (
                3 * i >= 1 * (0 + 0)
                and 3 * i < 1 * (0 + 6 * n + 0)
                and (
                    3 * i >= 1 * (0 + 0)
                    and 3 * i < 1 * (0 + 6 * n + 0)
                    and (
                        3 * i >= 1 * (0 + 0)
                        and 3 * i < 1 * (0 + 6 * n + 0)
                        and (3 * i < 1 * (0 + 12) and 3 * i > 1 * (0 + 2 * n + 0))
                    )
                )
            )
            for i in range(n + n)
        )
    )


def main():
    pass


if __name__ == "__main__":
    main()
