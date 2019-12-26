from typing import Callable, Iterable, T


def split_list(f: Callable[[T], int], lst: Iterable[T], amount=2):
    """
    splits the list into several list according to the function f

    :param lst: the list to split
    :param f: a function which maps from an argument to the index of the list it should go to
        for example if we wanted a function to split a list into a list of positive and negative number f could look like
        lambda x: int(x >= 0)
    :param amount: the amount of lists to split the data to (2 by default)
    :return: a tuple of all the lists created,
    """
    temp = tuple([] for _ in range(amount))
    for i in lst:
        temp[f(i)].append(i)
    return temp
