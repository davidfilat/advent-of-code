from functools import reduce
from typing import Dict
from utils.inputs import read_inputs
import re


ContainerStacksState = Dict[int, list[str]]
MoveType = tuple[int, int, int]


def get_intial_stack_state() -> ContainerStacksState:
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
    def parse_move(values):
        return tuple(map(int, values))

    pattern = re.compile(r"move (\d*) from (\d*) to (\d*)")
    return [parse_move(match.groups()) for match in pattern.finditer(text)]


def move_craters(
    crater_stacks: ContainerStacksState, move: MoveType
) -> ContainerStacksState:
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
    return reduce(move_craters, list_of_moves, stacks_state)


def get_top_craters_of_each_stack(stacks_state: ContainerStacksState) -> str:
    top_craters_of_each_stack = [stack[0] for stack in stacks_state.values()]
    return "".join(top_craters_of_each_stack)


if __name__ == "__main__":
    lines = read_inputs("day6.txt")
    stacks = get_intial_stack_state()
    moves = parse_moves(lines)
    final_stacks = apply_moves(stacks, moves)
    result = get_top_craters_of_each_stack(final_stacks)
    assert result == 'BRZGFVBTJ', 'You got the wrong answer!'
    print(result)
