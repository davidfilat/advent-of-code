from functools import partial, reduce
from operator import mul
from typing import Callable

from more_itertools import ilen
from toolz.functoolz import compose_left, curry, do, juxt

from utils.func import apply
from utils.inputs import read_inputs

THeight = int
TGrid = list[list[THeight]]
TTreeCoordinates = tuple[int, int]


def parse_tree_grid(text: str):
    lines = text.split("\n")
    return [list(map(int, line)) for line in lines]


def get_tree_rows_in_cardinal_directions(grid: TGrid, coordinates: TTreeCoordinates):
    row_index, col_index = coordinates
    row = grid[row_index]
    column = [row[col_index] for row in grid]
    return {
        "west": reversed(row[:col_index]),
        "east": row[col_index + 1 :],
        "north": reversed(column[:row_index]),
        "south": column[row_index + 1 :],
    }


def is_tree_on_the_edge_of_the_grid(grid: TGrid, coordinates: TTreeCoordinates):
    edge_indexes = {0, len(grid) - 1}
    return any(coordinate in edge_indexes for coordinate in coordinates)


def is_tree_the_highest_in_its_region(grid: TGrid, coordinates: TTreeCoordinates):
    trees_in_cardinal_directions = get_tree_rows_in_cardinal_directions(
        grid, coordinates
    )
    highest_trees_in_region = [
        max(row) for row in trees_in_cardinal_directions.values()
    ]
    row_index, col_index = coordinates
    return any(
        grid[row_index][col_index] > tree_height
        for tree_height in highest_trees_in_region
    )


def is_tree_visible(grid: TGrid) -> Callable[[TTreeCoordinates], bool]:
    return lambda tree: is_tree_on_the_edge_of_the_grid(
        grid, tree
    ) or is_tree_the_highest_in_its_region(grid, tree)


def find_visible_trees(grid: TGrid) -> list[TTreeCoordinates]:
    tree_coordinates = [
        (row_index, col_index)
        for row_index, row in enumerate(grid)
        for col_index, _ in enumerate(row)
    ]
    return list(filter(is_tree_visible(grid), tree_coordinates))


def find_index_first_tree_blocking_view(tree_height: int, row: list[int]) -> int | None:
    for index, height in enumerate(row):
        if height >= tree_height:
            return index + 1


def calculate_scenic_score(grid: TGrid, coordinates: TTreeCoordinates) -> int:
    row_index, col_index = coordinates
    tree_height = grid[row_index][col_index]
    viewing_distances = [
        find_index_first_tree_blocking_view(tree_height, direction) or ilen(direction)
        for direction in get_tree_rows_in_cardinal_directions(
            grid, coordinates
        ).values()
    ]
    return reduce(
        mul,
        viewing_distances,
        1,
    )


part_1: Callable[[str], int] = compose_left(
    parse_tree_grid,
    find_visible_trees,
    len,
    partial(do, partial(print, "The number of visible trees is:")),
)


part_2: Callable[[str], int] = compose_left(
    parse_tree_grid,
    juxt(curry(calculate_scenic_score), find_visible_trees),
    apply(map),
    max,
    partial(do, partial(print, "The highest scenic score is:")),
)


solve: Callable[[str], tuple[int, int]] = lambda raw_grid: (
    part_1(raw_grid),
    part_2(raw_grid),
)

if __name__ == "__main__":
    raw_grid = read_inputs("day8.txt")
    solve(raw_grid)
