from functools import partial, reduce
from typing import Callable

from toolz import compose_left, juxt

from utils.func import do_print
from utils.inputs import read_inputs


def are_all_characters_unique(sequence: str) -> bool:
    """
    are_all_characters_unique checks if all the characters in a string are unique

    Args:
        sequence (str): the input string

    Returns:
        bool: whether if all the characters in the string are unique
    """
    return len(set(sequence)) == len(sequence)


def find_marker(marker_length: int, message_stream: str) -> int | None:
    """
    find_marker finds the index of the first character in a sequence of unique characters of the given length

    Args:
        marker_length (int): the length for the sequence of unique characters
        message_stream (str): the input message string

    Returns:
        int | None: the index of the first character in marker sequence 
        or None if no marker is found
    """

    def find_maker_start_index(accumulator: None | int, start_index: int) -> int:
        if isinstance(accumulator, int):
            return accumulator
        end_of_sequence = start_index + marker_length
        sequence = message_stream[start_index:end_of_sequence]
        is_marker = are_all_characters_unique(sequence)
        return end_of_sequence if is_marker else accumulator

    return reduce(find_maker_start_index, range(len(message_stream)), None)


part_1 = compose_left(
    partial(find_marker, 4),
    do_print("The start of the 4 character packet marker is at index {}."),
)

part_2 = compose_left(
    partial(find_marker, 14),
    do_print("The start of the 14 character message marker is at index {}."),
)

solution: Callable[[str], tuple[int, int]] = juxt(part_1, part_2)

if __name__ == "__main__":
    raw_input = read_inputs("day6.txt")
    solution(raw_input)
