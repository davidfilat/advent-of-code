import re
from functools import reduce, partial
from typing import Dict, Callable

from toolz.functoolz import compose_left

from utils.func import do_print
from utils.inputs import read_inputs

ContainerStacksState = Dict[int, list[str]]
MoveType = tuple[int, int, int]


def get_intial_stack_state() -> ContainerStacksState:
    """
    get_intial_stack_state get the initial state of the container stacks

    Returns:
        ContainerStacksState: the initial state of the container stacks
    """
    intial_state = {
        1: "TZB",
        2: "NDTHV",
        3: "DMFB",
        4: "LQVWGJT",
        5: "MQFVPGDW",
        6: "SFHGQZV",
        7: "WCTLRNSZ",
        8: "MRNJDWHZ",
        9: "SDFLQM",
    }
    return {key: list(stack) for key, stack in intial_state.items()}


def parse_moves(text: str) -> list[MoveType]:
    """
    parse_moves parse the input string to tuples of integers

    Args:
        text (str): the input string with the instructions to move the craters

    Returns:
        list[MoveType]: a list of tuples of integers (number of craters to move, from stack, to stack)
    """

    def parse_move(values):
        return tuple(map(int, values))

    pattern = re.compile(r"move (\d*) from (\d*) to (\d*)")
    return [parse_move(match.groups()) for match in pattern.finditer(text)]


def move_craters(
    crater_stacks: ContainerStacksState, move: MoveType
) -> ContainerStacksState:
    """
    move_craters move the creater from one stack to another

    Args:
        crater_stacks (ContainerStacksState): the current state of the container stacks
        move (MoveType): the instruction to move the craters

    Returns:
        ContainerStacksState: the updated state of the container stacks
    """
    number_of_craters_to_move, from_stack, to_stack = move
    craters_to_move = crater_stacks[from_stack][0:number_of_craters_to_move]
    updated_stacks = (
        (from_stack, crater_stacks[from_stack][number_of_craters_to_move:]),
        (to_stack, craters_to_move + crater_stacks[to_stack]),
    )

    return crater_stacks | dict(updated_stacks)


def apply_moves(
    stacks_state: ContainerStacksState, list_of_moves: list[MoveType]
) -> ContainerStacksState:
    """
    apply_moves apply all the instruction to the container stacks state
    Args:
        stacks_state (ContainerStacksState): the initial state of the container stacks
        list_of_moves (list[MoveType]): the list of instructions to move the craters

    Returns:
        ContainerStacksState: the final state of the container stacks
    """
    return reduce(move_craters, list_of_moves, stacks_state)


def get_top_craters_of_each_stack(stacks_state: ContainerStacksState) -> str:
    """
    get_top_craters_of_each_stack get the letter marks of the top craters of each stack

    Args:
        stacks_state (ContainerStacksState): the state of the container stacks

    Returns:
        str: the letter marks of the top craters of each stack
    """
    top_craters_of_each_stack = [stack[0] for stack in stacks_state.values()]
    return "".join(top_craters_of_each_stack)


solution: Callable[[str], str] = compose_left(
    parse_moves,
    partial(apply_moves, get_intial_stack_state()),
    get_top_craters_of_each_stack,
    do_print("The top craters of each stack are: {}"),
)

if __name__ == "__main__":
    raw_instructions = read_inputs("day5.txt")
    result = solution(raw_instructions)
    assert result == "BRZGFVBTJ", "You got the wrong answer!"
