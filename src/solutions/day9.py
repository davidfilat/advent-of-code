import re
from functools import reduce
from typing import TypedDict, Callable

from toolz import pipe

from utils.func import do_print
from utils.inputs import read_inputs

TPosition = tuple[int, int]
TMove = tuple[str, int]


def move_right(from_position: TPosition) -> TPosition:
    x, y = from_position
    return (x + 1, y)


def move_left(from_position: TPosition) -> TPosition:
    x, y = from_position
    return (x - 1, y)


def move_down(from_position: TPosition) -> TPosition:
    x, y = from_position
    return (x, y - 1)


def move_up(from_position: TPosition) -> TPosition:
    x, y = from_position
    return (x, y + 1)


class RopeTracker(TypedDict):
    positions_visited_by_head: list[TPosition]
    positions_visited_by_tail: list[TPosition]
    last_head_position: TPosition
    last_tail_position: TPosition


def check_if_tail_not_adjacent_to_head(head_position: TPosition, tail_position: TPosition, rope_length: int = 2) -> bool:
    x, y = tail_position
    return x not in range(head_position[0] - rope_length + 1, head_position[0] + rope_length) or \
        y not in range(head_position[1] - rope_length + 1, head_position[1] + rope_length)


def move_head(direction) -> Callable[[TPosition], TPosition]:
    direction_move_map = {
        'R': move_right,
        'L': move_left,
        'U': move_up,
        'D': move_down
    }

    return lambda head_position: direction_move_map[direction](head_position)


def move_rope(direction, head_position, tail_position):
    new_head_position = move_head(direction)(head_position)
    new_tail_position = head_position if check_if_tail_not_adjacent_to_head(new_head_position,
                                                                            tail_position) else tail_position
    return {
        'head_position': new_head_position,
        'tail_position': new_tail_position
    }


def apply_move(tracker: RopeTracker, move: TMove) -> RopeTracker:
    direction, steps = move

    def apply_step(local_tracker: RopeTracker, _: int) -> RopeTracker:
        new_positions = move_rope(direction, local_tracker['last_head_position'], local_tracker['last_tail_position'])
        return {
            'positions_visited_by_head': local_tracker['positions_visited_by_head'] + [new_positions['head_position']],
            'positions_visited_by_tail': local_tracker['positions_visited_by_tail'] + [new_positions['tail_position']],
            'last_head_position': new_positions['head_position'],
            'last_tail_position': new_positions['tail_position']
        }

    return reduce(apply_step, range(steps), tracker)


def apply_moves(moves: list[TMove]):
    start_position = (0, 0)
    return reduce(apply_move, moves, {
        'positions_visited_by_head': [],
        'positions_visited_by_tail': [],
        'last_head_position': start_position,
        'last_tail_position': start_position
    })


def parse_moves(raw_input: str) -> list[TPosition]:
    def parse_move(match) -> TPosition:
        direction, steps = match.groups()
        return direction, int(steps)

    pattern = re.compile(r"([A-Z]) (\d*)")

    return [parse_move(match) for match in pattern.finditer(raw_input)]


def part_1(raw_input: str):
    return pipe(raw_input,
                parse_moves,
                apply_moves,
                lambda tracker: tracker['positions_visited_by_tail'],
                set,
                len,
                do_print('The tail of a 2-knot rope has visited {} positions')
                )


if __name__ == "__main__":
    raw_moves = read_inputs("day9.txt")
    part_1(raw_moves)
