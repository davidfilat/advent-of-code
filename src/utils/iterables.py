from typing import Iterable

from toolz import curry


@curry
def join_to_str(sep: str, iterable: Iterable) -> str:
    """
    join_to_str join an iterable to a string
    Args:
        sep (str): the separator to use 
        iterable (Iterable): the iterable to join (ex: [1, 2, 3]

    Returns:
        str: the joined string
    """
    return sep.join(iterable)
