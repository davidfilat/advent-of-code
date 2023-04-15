import operator
import re
from copy import deepcopy
from dataclasses import dataclass
from functools import partial
from typing import Callable, Final
from toolz import curry, compose_left, pipe, juxt
from toolz.curried import reduce, take, map

from utils.func import apply, do_print
from utils.inputs import read_inputs


@dataclass
class Monkey:
    id: int
    items: list[int]
    throw_to_if_true: int
    throw_to_if_false: int
    inspect_operation: Callable[[int], int]
    test_denominator: int
    items_inspected: int = 0

    def __init__(self, data: str):
        for line in data.splitlines():
            line = line.strip()
            match line.split(" "):
                case ["Monkey", ID]:
                    self.id = int(ID[:-1])
                case ["Starting", "items:", *_]:
                    self.items = [int(item) for item in re.findall(r"\d+", line)]
                case ["Operation:", "new", "=", _old, operation, value]:
                    self.inspect_operation = lambda x: OPERATIONS_MAP[operation](
                        x, int(value) if value != "old" else x
                    )
                case ["Test:", "divisible", "by", denominator]:
                    self.test_denominator = int(denominator)
                case ["If", "true:", "throw", "to", "monkey", monkey_id]:
                    self.throw_to_if_true = int(monkey_id)
                case ["If", "false:", "throw", "to", "monkey", monkey_id]:
                    self.throw_to_if_false = int(monkey_id)


class MonkeyGroup(list[Monkey]):
    pass


OPERATIONS_MAP: Final = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
}


def parse_input(text: str) -> MonkeyGroup:
    return MonkeyGroup([Monkey(data) for data in text.split("\n\n")])


def throw_item_to_monkey(
    item: int, monkey_id: int, monkey_group: MonkeyGroup
) -> MonkeyGroup:
    monkey_group[monkey_id].items.append(item)
    return monkey_group


@curry
def inspect_items(reduce_worry_func: Callable[[int], int], monkey: Monkey) -> Monkey:
    monkey.items = [
        reduce_worry_func(monkey.inspect_operation(item)) for item in monkey.items
    ]
    monkey.items_inspected += len(monkey.items)
    return monkey


@curry
def throw_items(monkey_group: MonkeyGroup, monkey: Monkey) -> Monkey:
    for item in monkey.items:
        if item % monkey.test_denominator == 0:
            throw_item_to_monkey(item, monkey.throw_to_if_true, monkey_group)
        else:
            throw_item_to_monkey(item, monkey.throw_to_if_false, monkey_group)
    monkey.items = []
    return monkey


@curry
def play_round(
    reduce_worry_func: Callable[[int], int], monkey_group: MonkeyGroup, _round_id: int
) -> MonkeyGroup:
    turn = compose_left(inspect_items(reduce_worry_func), throw_items(monkey_group))
    for monkey in monkey_group:
        turn(monkey)

    return monkey_group


def part_1(monkey_group: MonkeyGroup) -> int:
    def reduce_worry_func(x):
        return x // 3

    return pipe(
        monkey_group,
        deepcopy,
        lambda x: reduce(play_round(reduce_worry_func), range(20), x),
        map(lambda monkey: monkey.items_inspected),
        partial(sorted, reverse=True),
        take(2),
        apply(operator.mul),
        do_print("part 1: {}"),
    )


def part_2(monkey_group: MonkeyGroup) -> int:
    def reduce_worry_func(x):
        denominator = reduce(
            operator.mul, [monkey.test_denominator for monkey in monkey_group], 1
        )
        return x % denominator

    return pipe(
        monkey_group,
        deepcopy,
        lambda x: reduce(play_round(reduce_worry_func), range(10_000), x),
        map(lambda monkey: monkey.items_inspected),
        partial(sorted, reverse=True),
        take(2),
        apply(operator.mul),
        do_print("part 2: {}"),
    )


solution = juxt(part_1, part_2)

if __name__ == "__main__":
    raw_input = read_inputs("day11.txt")
    monkey_group = parse_input(raw_input)
    assert solution(monkey_group) == (50830, 14399640002)
