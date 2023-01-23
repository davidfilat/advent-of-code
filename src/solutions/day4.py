from typing import Iterable

from more_itertools import ilen
from toolz import juxt
from toolz.curried import map, pipe, filter

from utils.func import apply, do_print
from utils.inputs import read_inputs


def parse_range_pairs(range_pair_string: str) -> list[list[int]]:
    """
    parse_range_pairs parse a string representation of a list of range pairs (ex: "1-10,20-30") to a list of integers

    Args:
        range_pair_string (str): a string representation of a list of range pairs (ex: "1-10,20-30")

    Returns:
        list[list[int]]: the list of range lists

    """
    return [transform_str_to_range(range_string) for range_string in range_pair_string.split(",")]


def transform_str_to_range(range_string: str) -> list[int]:
    """
    transform_str_to_range transform a string representation of range (ex: "1-10") to a range object

    Args:
        range_string (str): a string representation of a range (ex: "1-10")

    Returns:
        range: a list of integers in the range

    """
    start, end = map(int, range_string.split("-"))
    return list(range(start, end + 1))


def sort_by_length(list_of_iterables: list[Iterable]) -> list[Iterable]:
    """
    sort_by_length sort the list by the length of the iterable elements
    Args:
        list_of_iterables: the list of iterables to sort

    Returns:
        list: the sorted list

    """
    return sorted(list_of_iterables, key=len)


def check_if_segments_include_each_other(segment1: list[int], segment2: list[int]) -> bool:
    """
    check_if_segments_include_each_other check if one segment is included in the other

    Args:
        segment1 (list[int]): the first segment
        segment2 (list[int]): the second segment

    Returns:
        bool: whether if one segment is included in the other

    """
    shortest_segment, longest_segment = sort_by_length([segment1, segment2])
    return all(element in longest_segment for element in shortest_segment)


def check_if_segments_overlap(segment1: list[int], segment2: list[int]) -> bool:
    """
    check_if_segments_overlap check if two segments overlap

    Args:
        segment1 (list[int]): the first segment
        segment2 (list[int]): the second segment

    Returns:
        bool: whether if the two segments overlap

    """
    shortest_segment, longest_segment = sort_by_length([segment1, segment2])
    return any(element in longest_segment for element in shortest_segment)


def part_1(raw_input: str):
    """
    part_1 finds out how many assignment pairs fully contain the other
    Args:
        raw_input: a list of string representation of range pairs (ex: "1-10,20-30")

    Returns:
        int: the number of assignment pairs that fully contain the other
    """
    return pipe(
        raw_input,
        lambda x: x.splitlines(),
        map(parse_range_pairs),
        filter(apply(check_if_segments_include_each_other)),
        ilen,
        do_print('There are {} assignment pairs that fully contain the other.')
    )


def part_2(raw_input: str):
    """
    part_2 finds out how many assignment pairs overlap
    Args:
        raw_input: a list of string representation of range pairs (ex: "1-10,20-30")

    Returns:
        int: the number of assignment pairs that overlap
    """
    return pipe(
        raw_input,
        lambda x: x.splitlines(),
        map(parse_range_pairs),
        filter(apply(check_if_segments_overlap)),
        ilen,
        do_print('There are {} assignment pairs that overlap.')
    )


solution = juxt(part_1, part_2)

if __name__ == "__main__":
    raw_instructions = read_inputs("day4.txt")
    solution(raw_instructions)
