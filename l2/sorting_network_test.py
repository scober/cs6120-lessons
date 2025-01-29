import itertools


def compare_and_swap(lst, l, r):
    assert r > l, f"right index ({r}) must be greater than left index ({l})"
    if lst[r] < lst[l]:
        tmp = lst[l]
        lst[l] = lst[r]
        lst[r] = tmp


def five_input_network(lst):
    # this network comes from here:
    # https://bertdobbelaere.github.io/sorting_networks.html#N5L9D5
    # but I believe the structures of short optimal sorting networks
    #   are relatively common knowledge
    assert len(lst) == 5
    compare_and_swap(lst, 0, 3)
    compare_and_swap(lst, 1, 4)
    compare_and_swap(lst, 0, 2)
    compare_and_swap(lst, 1, 3)
    compare_and_swap(lst, 0, 1)
    compare_and_swap(lst, 2, 4)
    compare_and_swap(lst, 1, 2)
    compare_and_swap(lst, 3, 4)
    compare_and_swap(lst, 2, 3)


def test():
    expected = [0, 1, 2, 3, 4]
    for perm in itertools.permutations(list(range(5))):
        perm = list(perm)
        five_input_network(perm)
        assert perm == expected, f"expected: {expected}, got: {perm}"
    print("success!")


if __name__ == "__main__":
    test()
