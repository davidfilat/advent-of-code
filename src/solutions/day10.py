from functools import reduce
from typing import Callable

from toolz import compose_left, juxt, curry

from utils.func import do_print
from utils.inputs import read_inputs

TRegisterValue = int
TRegisterCycles = list[TRegisterValue]
TCommand = Callable[[TRegisterValue], TRegisterCycles]


def apply_command(register: TRegisterCycles, command: TCommand) -> TRegisterCycles:
    *rest, current_register_value = register
    return [*register, *command(current_register_value)]


def apply_commands(commands: list[TCommand], init_register_value: TRegisterValue = 1) -> TRegisterCycles:
    return reduce(apply_command, commands, [init_register_value])


def get_signal_strength(at: int, register: TRegisterCycles) -> int:
    return register[at - 1] * at


@curry
def get_signal_strengths(at: list[int], register: TRegisterCycles) -> list[int]:
    return  [get_signal_strength(a, register) for a in at]


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


part_1: Callable[[str], int] = compose_left(parse_input,
                                            apply_commands,
                                            get_signal_strengths([20, 60, 100, 140, 180, 220]),
                                            sum,
                                            do_print("The sum of these six signal strengths is {}."))

part_2 = lambda x: 'To be implemented'

solve: Callable[[str], tuple[int, int]] = juxt(part_1, part_2)

if __name__ == "__main__":
    raw_commands = read_inputs("day10.txt")
    solve(raw_commands)
    # assert results == (6018, 2619), f'Wrong answers {results}'
