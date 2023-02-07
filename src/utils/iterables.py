from typing import Callable, Iterable


def join_to_str(sep: str) -> Callable[[Iterable], str]:
    """
    join_to_str join an iterable to a string
    Args:
        sep (str): the separator to use 

    Returns:
        str: the joined string
    """
    return lambda iterable: sep.join(iterable)