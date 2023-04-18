from typing import Optional

def make_move(message: str, board: list[list[str]], symbol: str) -> Optional[list[list[str]]]:
    """
    Return the updated board with the player's move if the move is valid, else return None.

    :param message: A string containing the row and column numbers separated by a space
    :param board: 3x3 list of lists representing the tic-tac-toe board
    :param symbol: The player's symbol, either 'X' or 'O'
    :return: The updated board if the move is valid, otherwise None
    """
    try:
        x, y = map(int, message.split(" "))
    except (ValueError, IndexError):
        return None
    if 1 <= x <= 3 and 1 <= y <= 3 and board[x - 1][y - 1] == '_':
        board[x - 1][y - 1] = symbol
        return board
    return None


def board_to_string(board: list[list[str]]) -> str:
    """
    Convert a 3x3 tic-tac-toe board to a formatted string representation.

    :param board: 3x3 list of lists representing the tic-tac-toe board
    :return: A formatted string representation of the board
    """
    return '\n' + '\n'.join([' '.join(row) for row in board]) + '\n'


def is_game_over(board: list[list[str]]) -> Optional[str]:
    """
    Check if the game is over.

    :param board: 3x3 list of lists representing the tic-tac-toe board
    :return: A string describing the result if the game is over, otherwise None
    """
    # Check if no moves left
    if not any('_' in row for row in board):
        return 'Game over. Draw'

    # Check if someone won
    for symbol in ('X', 'O'):
        # Check rows and columns
        for i in range(3):
            row_check = all(cell == symbol for cell in board[i])
            col_check = all(cell == symbol for cell in [board[j][i] for j in range(3)])
            if row_check or col_check:
                return f'Game over. Won {symbol}'
        # Check diagonals
        if all(board[i][i] == symbol for i in range(3)) or all(board[2 - i][i] == symbol for i in range(3)):
            return f'Game over. Won {symbol}'

    return None
