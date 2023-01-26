import string
from functools import partial
from typing import Callable

from toolz import juxt
from toolz.curried import map, pipe

from utils.func import apply, do_print
from utils.inputs import read_inputs


def get_letter_priority(letter: str) -> int:
    """
    get_letter_priority get the priority of the letter
    Args:
        letter (str): the letter to get the priority of

    Returns:
        int: the priority of the letter
    """
    return string.ascii_letters.index(letter) + 1


def split_in_half(sequence: str) -> tuple[str, str]:
    """
    split_in_half split the sequence in half

    Args:
        sequence (str): the sequence to split in half

    Returns:
        tuple[str, str]: the two halves of the sequence
    """
    length = len(sequence)
    return sequence[: length // 2], sequence[length // 2 :]


def get_list_intersection(list1: list, list2: list) -> list:
    """
    get_list_intersection get the intersection of two lists

    Args:
        list1 (list): the first list
        list2 (list): the second list

    Returns:
        list: the intersection of the two lists
    """
    return list(set(list1) & set(list2))


def split_into_chunks(chuck_size: int, sequence: str) -> list[str]:
    """
    split_into_chunks split the sequence into chunks of size chuck_size

    Args:
        chuck_size (int): the size of the chunks
        sequence (str): the sequence to split into chunks

    Returns:
        list[str]: the chunks of the sequence
    """
    return [sequence[i : i + chuck_size] for i in range(0, len(sequence), chuck_size)]


def sum_priority_per_bag(bag: str) -> int:
    """
    sum_priority_per_bag sum the priority of the letters in the bag

    Args:
        bag (str): the bag to sum the priority of the letters in

    Returns:
        int: the sum of the priority of the letters in the bag
    """
    return sum(get_letter_priority(letter) for letter in bag)


def deep_intersection(list_of_lists: list[list]) -> set:
    """
    deep_intersection get the intersection of a list of lists

    Args:
        list_of_lists (list[list]): the list of lists to get the intersection of

    Returns:
        list: the intersection of the list of lists
    """
    return set.intersection(*map(set, list_of_lists))


def part_1(raw_input: str) -> int:
    """
    part_1 return the sum of priority of the items
    that are in both compartments of the bag

    Args:
        raw_input (str): the raw input of the problem

    Returns:
        int: the sum of the priority of the letters
        that are found in both compartments of the bag
    """
    return pipe(
        raw_input,
        lambda s: s.splitlines(),
        map(split_in_half),
        map(apply(get_list_intersection)),
        map(set),
        map(sum_priority_per_bag),
        sum,
        do_print(
            "The sum of the priority of the items in both compartments of the bag is {}."
        ),
    )


def part_2(raw_input: str) -> int:
    """
    part_2 return the sum of priorities of badge items
    (badge items are items common in the bag of all three elfs in a group)

    Args:
        raw_input (str): the raw input of the problem

    Returns:
        int: the sum of the priorities of badge items
    """
    return pipe(
        raw_input,
        lambda s: s.splitlines(),
        partial(split_into_chunks, 3),
        map(deep_intersection),
        map(set),
        map(sum_priority_per_bag),
        sum,
        do_print("The sum of the priorities of badge items is {}."),
    )


solution: Callable[[str], tuple[int, int]] = juxt(part_1, part_2)

if __name__ == "__main__":
    raw_instructions = read_inputs("day3.txt")
    solution(raw_instructions)
