import re
from functools import reduce, partial
from typing import Callable

from more_itertools import last
from toolz import pipe, juxt
from toolz.curried import map

from utils.func import do_print
from utils.inputs import read_inputs

TPosition = tuple[int, int]
TMove = tuple[str, int]
TRope = list[TPosition]


def move_right(from_position: TPosition) -> TPosition:
    x, y = from_position
    return x + 1, y


def move_left(from_position: TPosition) -> TPosition:
    x, y = from_position
    return x - 1, y


def move_down(from_position: TPosition) -> TPosition:
    x, y = from_position
    return x, y - 1


def move_up(from_position: TPosition) -> TPosition:
    x, y = from_position
    return x, y + 1


def are_knots_adjacent(head: TPosition, tail: TPosition) -> bool:
    x, y = tail
    return x in range(head[0] - 1, head[0] + 2) and \
        y in range(head[1] - 1, head[1] + 2)


def move_knot(direction) -> Callable[[TPosition], TPosition]:
    direction_move_map = {
        'R': move_right,
        'L': move_left,
        'U': move_up,
        'D': move_down
    }

    return lambda head_position: direction_move_map[direction](head_position)


def get_number_sign(number: int) -> int:
    return 1 if number > 0 else -1


def steps_to_move(number: int) -> int:
    delta = abs(number)
    return delta - 1 if delta >= 2 else delta


def get_delta_for_axis(number: int) -> int:
    return steps_to_move(number) * get_number_sign(number)


def get_change_for_knot(knot_position: TPosition, head_knot_position: TPosition) -> tuple[int, int]:
    kx, ky = knot_position
    hx, hy = head_knot_position
    delta_x, delta_y = hx - kx, hy - ky

    delta_to_move = get_delta_for_axis(delta_x), get_delta_for_axis(delta_y)
    return delta_to_move


def keep_knot_close(knot_position: TPosition, head_knot_position: TPosition) -> TPosition:
    move_delta_for_knot = get_change_for_knot(knot_position, head_knot_position)
    position_with_the_delta_to_move = zip(knot_position, move_delta_for_knot)
    return tuple(map(sum, position_with_the_delta_to_move))


def move_rope(direction, rope: TRope) -> TRope:
    head_position, neck_position, *tail = rope

    new_head_position = move_knot(direction)(head_position)
    new_neck_position = neck_position if \
        are_knots_adjacent(new_head_position, neck_position) \
        else head_position

    def move_rest_of_rope(new_rope: TRope, previous_knot_position: TPosition) -> TRope:
        *rest, current_head_knot = new_rope
        new_tail_position = previous_knot_position if \
            are_knots_adjacent(current_head_knot, previous_knot_position) \
            else keep_knot_close(previous_knot_position, current_head_knot)
        return [*new_rope, new_tail_position]

    return reduce(move_rest_of_rope, tail, [new_head_position, new_neck_position])


def apply_move(tracker: list[TRope], move: TMove) -> list[TRope]:
    direction, steps = move

    def apply_step(local_tracker: list[TRope], _: int) -> list[TRope]:
        new_positions = move_rope(direction, local_tracker[-1])
        return local_tracker + [new_positions]

    return reduce(apply_step, range(steps), tracker)


def apply_moves(rope_length: int) -> Callable[[list[TMove]], list[TRope]]:
    start_position = (0, 0)
    rope = [start_position for _ in range(rope_length)]
    return lambda moves: reduce(apply_move, moves, [rope])


def parse_moves(raw_input: str) -> list[TPosition]:
    def parse_move(match) -> TPosition:
        direction, steps = match.groups()
        return direction, int(steps)

    pattern = re.compile(r"([A-Z]) (\d*)")

    return [parse_move(match) for match in pattern.finditer(raw_input)]


def solution(rope_length: int, raw_input: str):
    return pipe(raw_input,
                parse_moves,
                apply_moves(rope_length),
                map(last),
                set,
                len,
                do_print(f'The tail of a {rope_length}-knot rope '
                         + 'has visited {} positions')
                )


part_1 = partial(solution, 2)
part_2 = partial(solution, 10)

solve = juxt(part_1, part_2)

if __name__ == "__main__":
    raw_moves = read_inputs("day9.txt")
    solve(raw_moves)
