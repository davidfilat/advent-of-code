import sys

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
                    max(row[: col_index]),
                    max(row[col_index + 1:]),
                    max(column[: row_index]),
                    max(column[row_index + 1:]),
                ]
                tree = row[col_index]
                if any(tree > tree_height for tree_height in highest_trees_in_region):
                    visible_trees.append((row_index, col_index))
    return set(visible_trees)

solution_1 = compose_left(
    parse_tree_grid,
    find_visible_trees,
    len,
    partial(print, 'The number of visible trees is:'),
)

solution_2 = compose_left(
    parse_tree_grid,
    find_visible_trees,
    len,
    partial(print, 'The number of visible trees is:'),
)

if __name__ == "__main__":
    raw_grid = read_inputs("day8.txt")
    solution_1(raw_grid)
    solution_2(raw_grid)
