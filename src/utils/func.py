from pprint import pprint
from typing import Callable, TypeVar

TReturn = TypeVar("TReturn")


def apply(func: Callable[..., TReturn]) -> Callable[[tuple], TReturn]:
    return lambda args: func(*args)


TValue = TypeVar("TValue")


def do_print(phrase: str):
    """

    Args:
        phrase: a phrase that can be formatted with the value

    Returns:
        a function that prints the phrase with the value and returns the value

    """

    def print_and_return_value(value: TValue) -> TValue:
        print(phrase.format(value))
        return value

    return print_and_return_value


def do_pprint(obj: TValue) -> TValue:
    pprint(obj)
    return obj
