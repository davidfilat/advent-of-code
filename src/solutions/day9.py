import re

from utils.inputs import read_inputs

start_position = (0, 0)

TMove = tuple[str, int]


def move_right(steps, from_position):
    x, y = from_position
    visited_positions = [(i + 1, y) for i in range(x, x + steps)]
    return visited_positions, visited_positions[-1]


def move_left(steps, from_position):\
    x, y = from_position
    visited_positions = [(i + 1, y) for i in range(x, x + steps)]

def move_down(steps, from_position):
    x, y = from_position
    visited_positions = [(i + 1, y) for i in range(x, x + steps)]
    return visited_positions, visited_positions[-1]


def move_up(steps, from_position):
    x, y = from_position
    visited_positions = [(i + 1, y) for i in range(x, x + steps)]
    return visited_positions, visited_positions[-1]


direction_move_map = {
    'R': move_right,
    'L': move_left,
    'U': move_up,
    'D': move_down
}


def parse_moves(raw_input: str) -> list[TMove]:
    def parse_move(match) -> TMove:
        direction, steps = match.groups()
        return direction, int(steps)

    pattern = re.compile(r"([A-Z]) (\d*)")

    return [parse_move(match) for match in pattern.finditer(raw_input)]


if __name__ == "__main__":
    raw_moves = read_inputs("day9.txt")
    moves = parse_moves(raw_moves)
    print(moves)
