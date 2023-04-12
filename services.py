
def make_move(message, board, symbol):
    """
    Return the board with the player's move if a move is valid, else return None
    """
    try:
        x, y = map(int, message.split(" "))
    except (ValueError, IndexError):
        return None
    if 1 <= x <= 3 and 1 <= y <= 3 and board[x - 1][y - 1] == '_':
        board[x - 1][y - 1] = symbol
        return board
    return None


# def send_message_with_length(socket, message):
#     encoded_message = message.encode()
#     message_length = len(encoded_message)
#     socket.sendall(message_length.to_bytes(4, 'big'))
#     socket.sendall(encoded_message)
#
#
# def get_message_with_length(socket):
#     message_length = int.from_bytes(socket.recv(4), 'big')
#     response = socket.recv(message_length)
#     return response.decode()


# def print_board(board):
#     """Print the Tic-Tac-Toe board."""
#     for row in board:
#         print(' '.join(row))
#

# def get_move(player):
#     """Get a valid move (row and column) from the current player."""
#     while True:
#         try:
#             x, y = map(int, input(f'Player {player}. Please row and column (1-3) separated by space\n').split())
#             return x, y
#         except (ValueError, IndexError):
#             print('Invalid input. Retry')


# def make_move(player, board):
#     """Update the board with the player's move."""
#     while True:
#         x, y = get_move(player)
#         if board[x - 1][y - 1] == '_':
#             board[x - 1][y - 1] = player
#             return board
#         print('Please retry')


def is_game_over(symbol, board):
    """Checks if the game ended in a win"""
    # Check rows and columns
    for i in range(3):
        row_check = all(cell == symbol for cell in board[i])
        col_check = all(cell == symbol for cell in [board[j][i] for j in range(3)])
        if row_check or col_check:
            return True
    # Check diagonals
    if all(board[i][i] == symbol for i in range(3)) or all(board[2 - i][i] == symbol for i in range(3)):
        return True

    return False
