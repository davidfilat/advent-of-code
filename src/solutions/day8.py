import sys

from utils.inputs import read_inputs


def parse_tree_grid(text: str):
    lines = text.split('\n')
    return [list(line) for line in lines]


if __name__ == "__main__":
    raw_grid = read_inputs("day8.txt")
    grid = parse_tree_grid(raw_grid)
    print(grid)
