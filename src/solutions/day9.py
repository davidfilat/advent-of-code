import re
from functools import reduce, partial
from typing import Callable, cast, Literal

from more_itertools import last
from toolz import pipe, juxt, curry

from utils.func import do_print
from utils.inputs import read_inputs

TPosition = tuple[int, int]
TDirection = Literal["R", "L", "U", "D"]
TMove = tuple[TDirection, int]
TRope = list[TPosition]


def move_right(from_position: TPosition) -> TPosition:
    """
    move_right move the knot one position to the right

    Args:
        from_position (TPosition): tuple of x and y coordinates

    Returns:
        TPosition: tuple of x and y coordinates
    """
    x, y = from_position
    return x + 1, y


def move_left(from_position: TPosition) -> TPosition:
    """
    move_right move the knot one position to the left

    Args:
        from_position (TPosition): tuple of x and y coordinates

    Returns:
        TPosition: tuple of x and y coordinates
    """
    x, y = from_position
    return x - 1, y


def move_down(from_position: TPosition) -> TPosition:
    """
    move_right move the knot one position down

    Args:
        from_position (TPosition): tuple of x and y coordinates

    Returns:
        TPosition: tuple of x and y coordinates
    """
    x, y = from_position
    return x, y - 1


def move_up(from_position: TPosition) -> TPosition:
    """
    move_right move the knot one position up

    Args:
        from_position (TPosition): tuple of x and y coordinates

    Returns:
        TPosition: tuple of x and y coordinates
    """
    x, y = from_position
    return x, y + 1


def are_knots_adjacent(head: TPosition, tail: TPosition) -> bool:
    """
    are_knots_adjacent checks if two knots are adjacent

    Args:
        head (TPosition): tuple of x and y coordinates of the head knot
        tail (TPosition): tuple of x and y coordinates of the tail knot

    Returns:
        bool: True if the knots are adjacent, False otherwise
    """
    tx, ty = tail
    hx, hy = head
    return tx in range(hx - 1, hx + 2) and ty in range(hy - 1, hy + 2)


@curry
def move_head_knot(direction: TDirection, head_position: TPosition) -> TPosition:
    """
    move_head_knot get the function that moves the head knot in the given direction

    Args:
        direction (TDirection): direction to move the head knot (R, L, U, D)
        head_position (TPosition): tuple of x and y coordinates of the head knot

    Returns:
        TPosition: tuple of new x and y coordinates of the head knot
    """
    direction_move_map: dict[TDirection, Callable[[TPosition], TPosition]] = {
        "R": move_right,
        "L": move_left,
        "U": move_up,
        "D": move_down,
    }

    return direction_move_map[direction](head_position)


def get_change_for_knot(
    knot_position: TPosition, head_knot_position: TPosition
) -> tuple[int, int]:
    """
    get_change_for_knot calculate the change needed to move the knot to be adjacent to the head knot

    Args:
        knot_position (TPosition): a tuple of x and y coordinates of the knot
        head_knot_position (TPosition): a tuple of x and y coordinates of the head knot

    Returns:
        tuple[int, int]: the x and y deltas needed to move the knot to be adjacent to the head knot
    """
    kx, ky = knot_position
    hx, hy = head_knot_position
    delta_x, delta_y = hx - kx, hy - ky

    def direction_sign(number: int) -> int:
        return 1 if number >= 0 else -1

    def steps_to_move(number: int) -> int:
        delta = abs(number)
        return delta - 1 if delta >= 2 else delta

    def get_change_for_axis(number: int) -> int:
        return steps_to_move(number) * direction_sign(number)

    delta_to_move = get_change_for_axis(delta_x), get_change_for_axis(delta_y)
    return delta_to_move


def keep_knot_close(
    knot_position: TPosition, head_knot_position: TPosition
) -> TPosition:
    """
    keep_knot_close move the knot to be adjacent to the head knot

    Args:
        knot_position (TPosition): tuple of x and y coordinates of the knot
        head_knot_position (TPosition): tuple of x and y coordinates of the head knot

    Returns:
        TPosition: tuple of the new x and y coordinates of the knot
    """
    move_delta_for_knot = get_change_for_knot(knot_position, head_knot_position)
    position_with_the_delta_to_move = zip(knot_position, move_delta_for_knot)
    return cast(TPosition, tuple(map(sum, position_with_the_delta_to_move)))


def move_rope(direction: TDirection, rope: TRope) -> TRope:
    """
    move_rope move the rope in the given direction

    Args:
        direction (TDirection): direction to move the rope in (R, L, U, D)
        rope (TRope): a list of tuples of x and y coordinates of the rope knots

    Returns:
        TRope: a list of tuples of x and y coordinates of the rope knots after the move
    """
    head_position, neck_position, *tail = rope

    new_head_position = move_head_knot(direction)(head_position)
    new_neck_position = (
        neck_position
        if are_knots_adjacent(new_head_position, neck_position)
        else head_position
    )

    def move_rest_of_rope(new_rope: TRope, previous_knot_position: TPosition) -> TRope:
        *rest, current_head_knot = new_rope
        new_tail_position = (
            previous_knot_position
            if are_knots_adjacent(current_head_knot, previous_knot_position)
            else keep_knot_close(previous_knot_position, current_head_knot)
        )
        return [*new_rope, new_tail_position]

    return reduce(move_rest_of_rope, tail, [new_head_position, new_neck_position])


def apply_move(rope_tracker: list[TRope], move: TMove) -> list[TRope]:
    """
    apply_move apply a move to the rope

    Args:
        rope_tracker (list[TRope]): a list containing all the positions of the rope
        move (TMove): a tuple containing the direction and the number of steps to move

    Returns:
        list[TRope]: updated list of the rope positions
        containing all the new positions after applying the move
    """
    direction, steps = move

    def apply_step(local_rope_tracker: list[TRope], _: int) -> list[TRope]:
        new_positions = move_rope(direction, local_rope_tracker[-1])
        return local_rope_tracker + [new_positions]

    return reduce(apply_step, range(steps), rope_tracker)


@curry
def apply_moves(rope_length: int, moves: list[TMove]) -> list[TRope]:
    """
    apply_moves generates the rope and
    returns a function that applies the moves to the rope

    Args:
        rope_length (int): the length of the rope to generate
        moves (list[TMove]): a list of moves to apply to the rope

    Returns:
        list[TRope]: a list of the rope positions after applying the moves
    """
    start_position = (0, 0)
    rope = [start_position for _ in range(rope_length)]
    return reduce(apply_move, moves, [rope])


def parse_moves(raw_input: str) -> list[TMove]:
    """
    parse_moves parse the input into a list of moves

    Args:
        raw_input (str): the raw input of the challenge

    Returns:
        list[tuple[TDirection, int]]: a list of moves (direction, steps)
    """

    def parse_move(match) -> TMove:
        direction, steps = match.groups()
        return direction, int(steps)

    pattern = re.compile(r"([A-Z]) (\d*)")

    return [parse_move(match) for match in pattern.finditer(raw_input)]


@curry
def solution(rope_length: int, raw_input: str) -> int:
    """
    solution find the total number of positions visited by the tail
    of the rope at least once

    Args:
        rope_length (int): the length of the rope
        raw_input (str): the raw input containing the list of moves

    Returns:
        int: the total number of positions visited by the tail of the rope at least once
    """
    return pipe(
        raw_input,
        parse_moves,
        apply_moves(rope_length),
        partial(map, last),
        set,
        len,
        do_print(
            f"The tail of a {rope_length}-knot rope " + "has visited {} positions"
        ),
    )


part_1 = solution(2)
part_2 = solution(10)

solve = juxt(part_1, part_2)

if __name__ == "__main__":
    raw_moves = read_inputs("day9.txt")
    results = solve(raw_moves)
    assert results == (6018, 2619), f"Wrong answers {results}"
