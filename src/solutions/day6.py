import sys

from utils.inputs import read_inputs


def are_all_characters_unique(input: str) -> bool:
    """
    are_all_characters_unique checks if all the characters in a string are unique

    Args:
        input (str): the input string

    Returns:
        bool: whether if all the characters in the string are unique
    """
    return len(set(input)) == len(input)


def find_marker(marker_length: int, input: str, start_index: int = 0) -> int:
    """
    find_marker finds the index of the first charachter in a sequence of unique characters of the given length

    Args:
        marker_length (int): the length for the sequence of unique characters
        input (str): the input message string
        start_index (int, optional): the message index from which to start the check. Defaults to 0.

    Returns:
        int: the index of the first character in marker sequenece
    """
    end_of_sequence = start_index + marker_length
    sequence = input[start_index:end_of_sequence]
    is_marker = are_all_characters_unique(sequence)
    return (
        end_of_sequence
        if is_marker
        else find_marker(marker_length, input, start_index + 1)
    )


if __name__ == "__main__":
    input = read_inputs("day6.txt")
    sys.setrecursionlimit(len(input))
    start_of_packet_marker = find_marker(4, input)
    start_of_message_marker = find_marker(14, input)
    print("The start of the packet marker is at index", start_of_packet_marker, ".")
    print("The start of the message marker is at index", start_of_message_marker, ".")
