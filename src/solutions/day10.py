from functools import reduce
from typing import Callable

from toolz import compose_left, juxt, curry
from toolz.curried import partition

from utils.func import do_print
from utils.inputs import read_inputs
from utils.iterables import join_to_str

TRegisterValue = int
TRegisterCycles = list[TRegisterValue]
TCommand = Callable[[TRegisterValue], TRegisterCycles]

SCREEN_COLUMNS = 40
SCREEN_ROWS = 6
TSCREEN = list[list[str]]


def apply_command(register: TRegisterCycles, command: TCommand) -> TRegisterCycles:
    """
    apply_command apply a command to a register
    Args:
        register (TRegisterCycles): the register to add the command to
        command (TCommand): the command to apply

    Returns:
        TRegisterCycles: the register with the command added

    """
    *rest, current_register_value = register
    return [*register, *command(current_register_value)]


def apply_commands(
    commands: list[TCommand], init_register_value: TRegisterValue = 1
) -> TRegisterCycles:
    """
    apply_commands apply a list of commands to a register
    Args:
        commands (list[TCommand]): the list of commands to apply
        init_register_value (TRegisterValue): the initial value of the register

    Returns:
        TRegisterCycles: the register with all commands applied
    """
    return reduce(apply_command, commands, [init_register_value])


def get_signal_strength(at: int, register: TRegisterCycles) -> int:
    """
    get_signal_strength get the signal strength at a given cycle
    Args:
        at (int): the cycle to get the signal strength at
        register (TRegisterCycles): the register to get the signal strength from

    Returns:
        int: the signal strength at the given cycle
    """
    return register[at - 1] * at


@curry
def get_signal_strengths(at: list[int], register: TRegisterCycles) -> list[int]:
    """
    get_signal_strengths get the signal strength at a given cycles
    Args:
        at (list[int]): the cycles to get the signal strength at
        register (TRegisterCycles): the register to get the signal strength from

    Returns:
        list[int]: the signal strengths at the given cycles
    """
    return [get_signal_strength(a, register) for a in at]


def prepare_command(command: str) -> TCommand:
    """
    prepare_command prepare a command to be applied to a register
    Args:
        command (str): the command in string format (ex: "addx 1")

    Returns:
        TCommand: the command to be applied to a register
    """
    match command.split(" "):
        case ["noop"]:
            return lambda x: [x]
        case ["addx", x]:
            return lambda y: [int(y), y + int(x)]
        case _:
            raise ValueError(f"Unknown command {command}")


def parse_input(raw_input: str) -> list[TCommand]:
    """
    parse_input parse the input to a list of commands
    Args:
        raw_input (str): the input to parse

    Returns:
        list[TCommand]: the list of commands to apply to a register
    """
    commands = raw_input.splitlines()
    return list(map(prepare_command, commands))


def get_pixel(cycle: int, x: int) -> str:
    """
    get_pixel get the pixel to display at a given cycle and x position
    Args:
        cycle (int): the cycle to get the pixel at
        x (int): the value of the X register at the given cycle

    Returns:
        str: the pixel to display
    """
    return "█" if cycle % SCREEN_COLUMNS in range(x - 1, x + 2) else " "


def generate_crt(register: TRegisterCycles) -> TSCREEN:
    """
    generate_crt generate the CRT screen from a list register values
    Args:
        register (TRegisterCycles): the list of register values

    Returns:
        TSCREEN: the CRT screen (matrix format)
    """
    return partition(
        SCREEN_COLUMNS, [get_pixel(cycle, x) for cycle, x in enumerate(register)]
    )


def generate_screen_output(screen: TSCREEN) -> str:
    """
    generate_screen_output generate the screen output from a CRT screen
    Args:
        screen (TSCREEN): the CRT screen

    Returns:
        str: the screen output
    """
    rows = map(join_to_str(""), screen)
    return join_to_str("\n", rows)


part_1: Callable[[str], int] = compose_left(
    parse_input,
    apply_commands,
    get_signal_strengths([20, 60, 100, 140, 180, 220]),
    sum,
    do_print("The sum of these six signal strengths is {}."),
)

part_2: Callable[[str], str] = compose_left(
    parse_input,
    apply_commands,
    generate_crt,
    generate_screen_output,
    do_print("The screen will display:\n{}"),
)

solve: Callable[[str], tuple[int, str]] = juxt(part_1, part_2)

if __name__ == "__main__":
    raw_commands = read_inputs("day10.txt")
    (part_1, _) = solve(raw_commands)
    assert part_1 == 11720, f"Wrong answers {part_1}"
