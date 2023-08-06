import typing


def binary_search(
    predicate: typing.Callable[[int], bool],
    lower_bound: int,
    upper_bound: int,
) -> typing.Optional[int]:
    """Find the positive integer threshold below which a search criteria is
    never satisfied and above which it is always satisfied.

    Parameters
    ----------
    predicate : callable object
        Returns whether an integer value satisfies the search criteria.
    lower_bound : int
        Lower bound for the binary search, inclusive.
    upper_bound : int
        Upper bound for the binary search, inclusive.

    Returns
    -------
    guess
        The lowest integer value that satisfies the search criteria, and None
        if upper_bound does not satisfy the search criteria or search range is
        empty (i.e., lower_bound > upper_bound).
    """

    if lower_bound > upper_bound:
        return None
    if lower_bound == upper_bound:
        if predicate(lower_bound):
            return lower_bound
        else:
            return None

    midpoint = (lower_bound + upper_bound) // 2

    if predicate(midpoint):
        return binary_search(predicate, lower_bound, midpoint)
    else:
        return binary_search(predicate, midpoint + 1, upper_bound)
