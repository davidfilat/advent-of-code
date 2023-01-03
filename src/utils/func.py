from typing import Callable, TypeVar

TReturn = TypeVar("TReturn")


def apply(func: Callable[..., TReturn]) -> Callable[[tuple], TReturn]:
    return lambda args: func(*args)
