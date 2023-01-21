from functools import partial, reduce
from operator import mul
from typing import Callable, Iterator

from more_itertools import ilen
from toolz.functoolz import compose_left, curry, do, juxt

from utils.func import apply
from utils.inputs import read_inputs

THeight = int
TGrid = list[list[THeight]]
TTreeCoordinates = tuple[int, int]


def parse_tree_grid(text: str) -> TGrid:
    """
    parse_tree_grid transform the string form of a grid into a two-dimensional matrix

    Args:
        text: tree height grid representation as a string

    Returns:
        a two-dimensional matrix of tree heights
    """
    lines = text.splitlines()
    return [list(map(int, line)) for line in lines]


def get_tree_rows_in_cardinal_directions(
        grid: TGrid, coordinates: TTreeCoordinates
) -> dict[str, list[THeight] | Iterator[THeight]]:
    """
    get_tree_rows_in_cardinal_directions extract the rows of tree heights in the 4 cardinal directions

    Args:
        grid: a two-dimensional matrix of tree heights
        coordinates: a tree coordinates

    Returns:
        a dictionary of the rows of tree heights in the 4 cardinal directions relative to the give tree coordinates
    """
    row_index, col_index = coordinates
    row = grid[row_index]
    column = [row[col_index] for row in grid]
    return {
        "west": reversed(row[:col_index]),
        "east": row[col_index + 1:],
        "north": reversed(column[:row_index]),
        "south": column[row_index + 1:],
    }


def is_tree_on_the_edge_of_the_grid(grid: TGrid, coordinates: TTreeCoordinates) -> bool:
    """
    is_tree_on_the_edge_of_the_grid checks if the tree is on the edge of the grid

    Args:
        grid: two-dimensional matrix of tree heights
        coordinates: tree coordinates inside the grid

    Returns:
        boolean indicating if the tree is on the edge of the grid
    """
    edge_indexes = {0, len(grid) - 1}
    return any(coordinate in edge_indexes for coordinate in coordinates)


def is_tree_the_highest_in_its_region(
        grid: TGrid, coordinates: TTreeCoordinates
) -> bool:
    """
    is_tree_the_highest_in_its_region checks if the tree is the highest in all 4 cardinal directions

    Args:
        grid: two-dimensional matrix of tree heights
        coordinates: tree coordinates inside the grid

    Returns:
        boolean indicating if the tree is the highest in all 4 cardinal directions
    """
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


def is_tree_visible_from_outside(grid: TGrid) -> Callable[[TTreeCoordinates], bool]:
    """
    is_tree_visible_from_outside checks if the

    Args:
        grid: two-dimensional matrix of tree heights

    Returns:
        a function that accepts a tree coordinates and returns a boolean indicating
        if the tree is visible from outside the grid
    """
    return lambda tree: is_tree_on_the_edge_of_the_grid(
        grid, tree
    ) or is_tree_the_highest_in_its_region(grid, tree)


def find_visible_trees(grid: TGrid) -> list[TTreeCoordinates]:
    """
    find_visible_trees find the coordinates of the trees that are visible outside the grid

    Args:
        grid: two-dimensional matrix of tree heights

    Returns:
        a list of tree coordinates that are visible outside the grid
    """
    tree_coordinates = [
        (row_index, col_index)
        for row_index, row in enumerate(grid)
        for col_index, _ in enumerate(row)
    ]
    return list(filter(is_tree_visible_from_outside(grid), tree_coordinates))


def find_index_first_tree_blocking_view(
        tree_height: int, row: list[THeight] | Iterator[THeight]
) -> int | None:
    """
    find_index_first_tree_blocking_view returns the index of the first tree that is
    of the same height or higher that the given tree

    Args:
        tree_height: given tree height
        row: list of tree heights
    Returns:
        the index of the first tree that is of the same height or higher
    """
    for index, height in enumerate(row):
        if height >= tree_height:
            return index + 1
    return None


def calculate_scenic_score(grid: TGrid, coordinates: TTreeCoordinates) -> int:
    """
    calculate_scenic_score returns the scenic score for a given tree in the grid

    Args:
        grid: a two-dimensional matrix of tree heights
        coordinates: given tree coordinates

    Returns:
        the scenic score of the given tree
        the product of the number of all visible trees in the 4 cardinal directions
    """
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


# Find the number of visible trees outside the grid
part_1: Callable[[str], int] = compose_left(
    parse_tree_grid,
    find_visible_trees,
    len,
    partial(do, partial(print, "The number of visible trees is:")),
)

# Find the highest scenic score for the grid
part_2: Callable[[str], int] = compose_left(
    parse_tree_grid,
    juxt(curry(calculate_scenic_score), find_visible_trees),
    apply(map),
    max,
    partial(do, partial(print, "The highest scenic score is:")),
)

solve: Callable[[str], tuple[int, int]] = juxt(part_1, part_2)

if __name__ == "__main__":
    raw_grid = read_inputs("day8.txt")
    solve(raw_grid)
