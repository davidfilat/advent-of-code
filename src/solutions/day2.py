from operator import eq
from typing import cast, Callable

from toolz import first, juxt, pipe
from toolz.curried import map

from utils.func import do_print
from utils.inputs import read_inputs

WINNING_COMBINATIONS = [
    (3, 1),
    (1, 2),
    (2, 3),
]

TRound = tuple[int, int]


def replace_moves_with_numbers(single_round: list[str]) -> TRound:
    """

    Args:
        single_round: a list of two letters marking the move of the opponent and yours

    Returns:
        a tuple of integers marking the score of the moves

    """

    def replace_move_with_number(move: str) -> int:
        match move:
            case "A" | "X":
                return 1
            case "B" | "Y":
                return 2
            case "C" | "Z":
                return 3
            case _:
                raise ValueError(f"Invalid move {move}")

    return cast(TRound, tuple(replace_move_with_number(move) for move in single_round))


def parse_rounds(raw_input: str) -> list[TRound]:
    """

    Args:
        raw_input: the raw input containing the rounds of the game

    Returns:
        a list of tuples of integers marking the score of the moves for each round

    """
    return [
        replace_moves_with_numbers(one_round.split(" "))
        for one_round in raw_input.splitlines()
    ]


def calculate_round_score(one_round: tuple[int, int]) -> int:
    """

    Args:
        one_round: the score of each the move of each player

    Returns:
        the score of the round

    """
    opponent_move, my_move = one_round
    if one_round in WINNING_COMBINATIONS:
        return 6 + my_move
    elif eq(my_move, opponent_move):
        return 3 + my_move
    else:
        return 0 + my_move


def get_winner_combination(opponent_move: int) -> tuple[int, int]:
    """

    Args:
        opponent_move: the score of the opponent's move

    Returns:
        the combination of moves that results in a win

    """
    return first(
        filter(
            lambda combination: combination[0] == opponent_move, WINNING_COMBINATIONS
        )
    )


def get_loser_combination(opponent_move: int) -> TRound:
    """

    Args:
        opponent_move:  the score of the opponent's move

    Returns:
        the combination of moves that results in a loss

    """
    loser_combination = pipe(
        filter(
            lambda combination: combination[1] == opponent_move, WINNING_COMBINATIONS
        ),
        first,
        reversed,
        tuple
    )

    return cast(TRound, loser_combination)


def calculate_round_outcome(one_round: tuple[int, int]) -> tuple[int, int]:
    """

    Args:
        one_round: a tuple of integers marking the score
        of the move of the opponent and the expected outcome

    Returns:
        the combination of moves that results in the expected outcome

    """
    outcome_map: dict[int, Callable[[int], TRound]] = {
        1: get_loser_combination,
        2: lambda move: (move, move),
        3: get_winner_combination,
    }
    opponent_move, outcome = one_round
    return outcome_map[outcome](opponent_move)


def part_1(raw_input: str) -> int:
    """

    Args:
        raw_input: the raw input containing the rounds of the game

    Returns:
        the total score of the game

    """
    result = pipe(
        raw_input,
        parse_rounds,
        map(calculate_round_score),
        sum,
        do_print("The total score would be {}."),
    )
    return cast(int, result)


def part_2(raw_input: str) -> int:
    """

    Args:
        raw_input: the raw input containing the rounds of the game

    Returns:
        the total score of the game if the strategy is followed

    """
    result = pipe(
        raw_input,
        parse_rounds,
        map(calculate_round_outcome),
        map(calculate_round_score),
        sum,
        do_print("According to the strategy, the total score would be {}."),
    )
    return cast(int, result)


solution = juxt(part_1, part_2)

if __name__ == "__main__":
    raw_instructions = read_inputs("day2.txt")
    results = solution(raw_instructions)
    assert results == (14297, 10498), f'Wrong answers {results}'