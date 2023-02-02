from functools import reduce
from typing import Callable

from toolz import compose_left, juxt

from utils.func import do_print
from utils.inputs import read_inputs

TCommand = Callable[[int], list[int]]


def apply_command(register: list[int], command: TCommand) -> list[int]:
    *rest, current_register_value = register
    return [*register, *command(current_register_value)]


def apply_commands(commands: list[TCommand], init_register_value: int = 1) -> list[int]:
    return reduce(apply_command, commands, [init_register_value])


def get_signal_strength(at: int, register: list[int]) -> int:
    return register[at - 1] * at


def get_signal_strengths(at: list[int]) -> Callable[[list[int]], list[int]]:
    return lambda register: [get_signal_strength(a, register) for a in at]


def prepare_command(command: str) -> TCommand:
    match command.split(" "):
        case ["noop"]:
            return lambda x: [x]
        case ["addx", x]:
            return lambda y: [int(y), y + int(x)]
        case _:
            raise ValueError(f"Unknown command {command}")


def parse_input(raw_input: str) -> list[TCommand]:
    commands = raw_input.splitlines()
    return list(map(prepare_command, commands))


part_1 = compose_left(parse_input,
                      apply_commands,
                      get_signal_strengths([20, 60, 100, 140, 180, 220]),
                      sum,
                      do_print("The sum of these six signal strengths is {}."))

part_2 = lambda x: 'To be implemented'

solve = juxt(part_1, part_2)

if __name__ == "__main__":
    raw_commands = read_inputs("day10.txt")
    solve(raw_commands)
    # assert results == (6018, 2619), f'Wrong answers {results}'
