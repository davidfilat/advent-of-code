from functools import reduce
from operator import concat, ge, le
from typing import Callable, TypeVar
from utils.inputs import read_inputs
from toolz import concat

TFolder = TypeVar("TFolder", bound="Folder")


class File:
    def __init__(self, name: str, parent: TFolder, size=0):
        self.name = name
        self.parent = parent
        self.size = size

    def get_path(self) -> str:
        return self.parent.get_path() + "/" + self.name

    def get_size(self) -> int:
        return self.size

    def __repr__(self):
        return f"File({self.name}, {self.parent})"

    def __str__(self):
        return self.get_path()


class Folder:
    def __init__(self, name: str, parent=None):
        self.name = name
        self.parent = parent
        self.children = []

    def add_child(self, child: TFolder | File):
        self.children.append(child)

    def get_size(self) -> int:
        if not len(self.children):
            return 0
        return sum(child.get_size() for child in self.children)

    def get_path(self) -> str:
        if self.parent is None:
            return ""
        else:
            return self.parent.get_path() + "/" + self.name

    def __repr__(self):
        return f"Folder({self.name}, {self.get_path()})"

    def __str__(self):
        return self.get_path()


def get_fs_root(folder: Folder):
    if folder.parent is None:
        return folder
    return get_fs_root(folder.parent)


def parse_command(command: str, cwd: Folder) -> Folder:
    if command.startswith("$ cd"):
        folder_name = command.split(" ")[2]
        if folder_name == "..":
            return cwd.parent
        if folder_name == "/":
            return get_fs_root(cwd)
        folder = Folder(folder_name, cwd)
        cwd.add_child(folder)
        return folder
    return cwd


def parse_line(cwd: Folder, line: str) -> Folder:
    if line.startswith("$"):
        return parse_command(line, cwd)
    if line and not line.startswith("dir"):
        [size, name] = line.split()
        file = File(name, cwd, int(size))
        cwd.add_child(file)
    return cwd


def parse_input(input: str) -> Folder:
    lines = input.split("\n")
    root = Folder("/", None)
    reduce(parse_line, lines, root)
    return root


def find_folders_matching_condition(
    comparison_operator: Callable, right_hand_comparison_value: int, folder: Folder
) -> list[Folder]:
    sub_folders = [c for c in folder.children if isinstance(c, Folder)]
    if not sub_folders and comparison_operator(
        folder.get_size(), right_hand_comparison_value
    ):
        return [folder]
    folders = [
        find_folders_matching_condition(
            comparison_operator, right_hand_comparison_value, sub_folder
        )
        for sub_folder in sub_folders
    ]

    if comparison_operator(folder.get_size(), right_hand_comparison_value):
        folders = [*folders, [folder]]

    return list(concat(folders))


def sum_folder_sizes(folders: list[Folder]):
    return sum(folder.get_size() for folder in folders)


def find_smallest_folder_to_delete(required_size: int, fs_root: Folder):
    folders = find_folders_matching_condition(ge, required_size, fs_root)
    return min(
        [folder.get_size() for folder in folders if folder.get_size() >= required_size]
    )


def get_needed_size(fs_root: Folder):
    TOTAL_MEMORY = 70_000_000
    REQUIRED_MEMORY = 30_000_000
    available_memory = TOTAL_MEMORY - root.get_size()
    return REQUIRED_MEMORY - available_memory


if __name__ == "__main__":
    input = read_inputs("day7.txt")
    root = parse_input(input)
    folders = find_folders_matching_condition(le, 100_000, root)
    result1 = sum_folder_sizes(folders)
    print("Result for part 1 is:", result1)

    result2 = find_smallest_folder_to_delete(get_needed_size(root), root)
    print("Result for part 2 is:", result2)
