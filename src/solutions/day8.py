from functools import reduce
from operator import mul
from typing import Literal

from utils.inputs import read_inputs

from toolz.functoolz import compose_left, do, partial


def parse_tree_grid(text: str):
    lines = text.split("\n")
    return [list(map(int, line)) for line in lines]


def find_visible_trees(grid: list[list[int]]):
    visible_trees = []
    for row_index, row in enumerate(grid):
        for col_index, _ in enumerate(row):
            column = [row[col_index] for row in grid]
            if row_index in (0, len(row) - 1) or col_index in (0, len(column) - 1):
                visible_trees.append((row_index, col_index))
            else:
                highest_trees_in_region = [
                    max(row[:col_index]),
                    max(row[col_index + 1 :]),
                    max(column[:row_index]),
                    max(column[row_index + 1 :]),
                ]
                tree = row[col_index]
                if any(tree > tree_height for tree_height in highest_trees_in_region):
                    visible_trees.append((row_index, col_index))
    return set(visible_trees)


def find_index_first_tree_blocking_view(tree_height: int, row: list[int]):
    def find_tree_blocking_view(acc: int | Literal[False], tree: tuple[int, int]):
        index, height = tree
        return index + 1 if height >= tree_height and not acc else acc

    return reduce(find_tree_blocking_view, enumerate(row), False)


def calculate_scenic_score(grid: list[list[int]], tree: tuple[int, int]):
    row_index, col_index = tree
    row = grid[row_index]
    column = [row[col_index] for row in grid]
    tree_height = row[col_index]
    west = list(reversed(row[:col_index]))
    east = row[col_index + 1 :]
    north = list(reversed(column[:row_index]))
    south = column[row_index + 1 :]

    viewing_distances = [
        find_index_first_tree_blocking_view(tree_height, direction) or len(direction)
        for direction in (west, east, north, south)
    ]

    return reduce(
        mul,
        viewing_distances,
        1,
    )


part_1 = compose_left(
    parse_tree_grid,
    find_visible_trees,
    len,
    partial(do, partial(print, "The number of visible trees is:")),
)


def part_2(input_grid: str):
    grid = parse_tree_grid(input_grid)
    calculate_scenic_score_per_tree = partial(calculate_scenic_score, grid)
    return compose_left(
        find_visible_trees,
        partial(map, calculate_scenic_score_per_tree),
        max,
        partial(do, print),
    )(grid)


if __name__ == "__main__":
    raw_grid = read_inputs("day8.txt")
    part_1(raw_grid)
    part_2(raw_grid)
