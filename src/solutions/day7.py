from abc import ABC, abstractmethod
from functools import reduce
from operator import ge, le
from typing import Callable, Self

from toolz import concat

from utils.inputs import read_inputs


class FSComponent(ABC):
    @abstractmethod
    def get_size(self):
        pass

    @abstractmethod
    def get_path(self):
        pass


class File(FSComponent):
    def __init__(self, name: str, parent: "Folder", size=0):
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


class Folder(FSComponent):
    def __init__(self, name: str, parent=None):
        self.name = name
        self.parent = parent
        self.children: list[File | Folder] = []

    def add_child(self, child: Self | File):
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


def get_fs_root(folder: Folder) -> Folder:
    """
    get_fs_root finds the root of the file system

    Args:
        folder (Folder): a folder in the file system

    Returns:
        Folder: the root of the file system
    """
    if folder.parent is None:
        return folder
    return get_fs_root(folder.parent)


def parse_command(command: str, cwd: Folder) -> Folder:
    """
    parse_command parses the shell command and updates the current working directory

    Args:
        command (str): the shell command output line
        cwd (Folder): the current working directory

    Returns:
        Folder: the new current working directory
    """
    if command.startswith("$ cd"):
        folder_name = command.split(" ")[2]
        if folder_name == "..":
            return cwd.parent or cwd
        if folder_name == "/":
            return get_fs_root(cwd)
        folder = Folder(folder_name, cwd)
        cwd.add_child(folder)
        return folder
    return cwd


def parse_line(cwd: Folder, line: str) -> Folder:
    """
    parse_line parse a single line from the shell output

    Args:
        cwd (Folder): the current working directory
        line (str): a single line of shell output

    Returns:
        Folder: the new or updated current working directory
    """
    if line.startswith("$"):
        return parse_command(line, cwd)
    if line and not line.startswith("dir"):
        [size, name] = line.split()
        file_leaf = File(name, cwd, int(size))
        cwd.add_child(file_leaf)
    return cwd


def parse_input(raw_input: str) -> Folder:
    """
    parse_input parse the input string into a file system tree

    Args:
        raw_input (str): the string containing the shell output from the device

    Returns:
        Folder: the file system root
    """
    lines = raw_input.splitlines()
    fs_root = Folder("/", None)
    reduce(parse_line, lines, fs_root)
    return fs_root


def find_folders_matching_condition(
        comparison_operator: Callable, right_hand_comparison_value: int, folder: Folder
) -> list[Folder]:
    """
    find_folders_matching_condition _summary_

    Args:
        comparison_operator (Callable): _description_
        right_hand_comparison_value (int): _description_
        folder (Folder): _description_

    Returns:
        list[Folder]: _description_
    """
    sub_folders = [c for c in folder.children if isinstance(c, Folder)]
    if not sub_folders and comparison_operator(
            folder.get_size(), right_hand_comparison_value
    ):
        return [folder]
    matching_folders = [
        find_folders_matching_condition(
            comparison_operator, right_hand_comparison_value, sub_folder
        )
        for sub_folder in sub_folders
    ]

    if comparison_operator(folder.get_size(), right_hand_comparison_value):
        matching_folders.append([folder])

    return list(concat(matching_folders))


def sum_folder_sizes(folder_list: list[Folder]) -> int:
    """
    sum_folder_sizes sums the sizes of a list of folders

    Args:
        folder_list (list[Folder]): a list of folders

    Returns:
        int: the sum of folder sizes
    """
    return sum(folder.get_size() for folder in folder_list)


def find_smallest_folder_to_delete(required_size: int, fs_root: Folder) -> int:
    """
    find_smallest_folder_to_delete find the size of the smallest folder that can be deleted to free enough memory

    Args:
        required_size (int): the amount of memory that needs freeing up
        fs_root (Folder): the file system root

    Returns:
        int: the size of the directory that can be deleted
    """
    matching_folders = find_folders_matching_condition(ge, required_size, fs_root)
    return min(
        [folder.get_size() for folder in matching_folders if folder.get_size() >= required_size]
    )


def get_needed_size(fs_root: Folder) -> int:
    """
    get_needed_size find the amount of memory that needs freeing up

    Args:
        fs_root (Folder): the root of the file system

    Returns:
        int: the amount of memory that needs freeing up
    """
    TOTAL_MEMORY = 70_000_000
    REQUIRED_MEMORY = 30_000_000
    available_memory = TOTAL_MEMORY - fs_root.get_size()
    return REQUIRED_MEMORY - available_memory


if __name__ == "__main__":
    shell_output = read_inputs("day7.txt")
    root = parse_input(shell_output)
    folders = find_folders_matching_condition(le, 100_000, root)
    result1 = sum_folder_sizes(folders)
    print("Result for part 1 is:", result1)

    result2 = find_smallest_folder_to_delete(get_needed_size(root), root)
    print("Result for part 2 is:", result2)
