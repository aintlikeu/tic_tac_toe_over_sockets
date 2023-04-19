import socket
import threading
from dataclasses import dataclass
from services import make_move, is_game_over, board_to_string
from exceptions import GameOverException, WrongMoveException
from config import SERVER_ADDRESS, SERVER_PORT, CLIENT_SYMBOL



@dataclass
class GameState:
    """
    A data class that represents the game state.

    The game state includes the list of connected clients, the current client, and the game board.
    """
    clients = []
    current_client = None
    board = [['_'] * 3 for _ in range(3)]


def send_greeting(client_id: int, client_socket: socket.socket) -> None:
    """
    Sends a greeting message to the client.

    :param client_id: An integer representing the client's ID (1 or 2)
    :param client_socket: A socket object representing the client's connection
    """
    message = f"Greetings in Tic-Tac-Toe! You play by '{CLIENT_SYMBOL[client_id]}'. "
    if client_id == 1:
        message += "Waiting for the second player"
    else:
        message += "Please wait"
    client_socket.sendall(message.encode())


def get_move(board: list[list[str]], client_id: int, client_socket: socket.socket) -> str:
    """
    Sends a message to the client to get their move and returns their response.

    :param board: A 3x3 list of lists representing the current state of the game board.
    :param client_id: An integer representing the client's ID (1 or 2)
    :param client_socket: A socket object representing the client's connection
    :return: A string representing the client's move
    :raises WrongMoveException: If the client sends an invalid move
    """
    message = f"\nBoard:{board_to_string(board)}\nYour move. " \
              f"Please type row and column (1-3) separated by space: "
    client_socket.sendall(message.encode())
    response = client_socket.recv(3)
    if not response:
        raise WrongMoveException
    data = response.decode()
    print(f"Message from client {client_id}: {data}")
    return data

def handle_game_over(game_state: GameState) -> bool:
    """
    Checks if the game is over and handles the end of the game.

    :param game_state: A GameState instance containing the shared game state, including clients, the current client,
                       and the board
    :return: True if the game is over and has been handled, False otherwise.
    :raises GameOverException: If the game is over and a winner is found, or it's a draw.
    """
    try:
        _ = is_game_over(game_state.board)
    except GameOverException as e:
        message = f"\n{e}\nFinal board:{board_to_string(game_state.board)}"
        for c in game_state.clients:
            c.sendall(message.encode())
            c.close()
        print(f"Game over. Connection closed with both players")
        return True
    return False


def handle_client(client_socket: socket.socket, address: tuple[str, int], client_id: int, game_state: GameState) -> None:
    """
    Handles the client's connection and game logic.

    :param game_state: A GameState instance containing the shared game state, including clients, the current client,
                       and the board
    :param client_socket: A socket object representing the client's connection
    :param address: A tuple containing the client's IP address and port number
    :param client_id: An integer representing the client's ID (1 or 2)
    """
    print(f"Connection established with player '{CLIENT_SYMBOL[client_id]}, address {address}'")

    if client_id == 1:
        game_state.current_client = client_socket

    send_greeting(client_id, client_socket)

    while True:
        if len(game_state.clients) == 2:
            other_client_socket = [c for c in game_state.clients if c != client_socket][0]

            if game_state.current_client == client_socket:
                # try to get move from the client
                try:
                    data = get_move(game_state.board, client_id, client_socket)
                except WrongMoveException:
                    continue
                updated_board = make_move(data, game_state.board, CLIENT_SYMBOL[client_id])
                # if the move was correct, update board
                if updated_board is not None:
                    game_state.board = updated_board
                    # check if the game is over
                    if handle_game_over(game_state):
                        break

                    # switch current client
                    message = f"Board after your move:{board_to_string(game_state.board)}\nPlease wait"
                    client_socket.sendall(message.encode())
                    game_state.current_client = other_client_socket


def main():
    game_state = GameState()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # reuse address if the OS hasn't released the port yet
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
    server_socket.listen(2)

    print("Server is listening for incoming connections...")
    clients_connected = 0
    while clients_connected < 2:
        client_socket, address = server_socket.accept()
        clients_connected += 1
        game_state.clients.append(client_socket)

        client_thread = threading.Thread(target=handle_client, args=(client_socket, address, clients_connected, game_state))
        client_thread.start()

    print("\nServer has reached the maximum number of players.")


if __name__ == '__main__':
    main()
