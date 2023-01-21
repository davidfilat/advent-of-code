from functools import partial

from toolz import compose_left, juxt
from toolz.curried import tail

from utils.inputs import read_inputs


def parse_calories_groups(raw_input: str) -> list[list[int]]:
    """

    Args:
        raw_input: a string with the calories of each elf grouped in paragraphs

    Returns:
        the calories grouped in a list for each elf

    """
    calories_groups = raw_input.split("\n\n")

    def parse_calories_group(calories_group: str) -> list[int]:
        calories = calories_group.splitlines()
        return [int(calorie) for calorie in calories]

    return list(map(parse_calories_group, calories_groups))


def get_sum_of_calories_per_elf(calories_groups: list[list[int]]) -> list[int]:
    """

    Args:
        calories_groups: a list of calories packed for each elf in the expedition

    Returns:
        the sum of all the calories each elf had packed

    """
    return list(map(sum, calories_groups))


part_1 = compose_left(parse_calories_groups,
                      get_sum_of_calories_per_elf,
                      max,
                      'The richest elf has {} calories.'.format,
                      print)

part_2 = compose_left(parse_calories_groups,
                      get_sum_of_calories_per_elf,
                      sorted,
                      tail(3),
                      sum,
                      'The three richest elves have {} calories in total.'.format,
                      print)

solution = juxt(part_1, part_2)

if __name__ == "__main__":
    raw_input = read_inputs("day1.txt")
    solution(raw_input)
