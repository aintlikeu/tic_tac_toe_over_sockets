import socket
import threading
from typing import Tuple
from services import make_move, is_game_over, board_to_string

CLIENT_SYMBOL = {1: 'X', 2: 'O'}

clients = []
current_client = None
board = [['_'] * 3 for _ in range(3)]


def handle_client(client_socket: socket.socket, address: Tuple[str, int], client_id: int) -> None:
    """
    Handles the client's connection and game logic.

    :param client_socket: A socket object representing the client's connection
    :param address: A tuple containing the client's IP address and port number
    :param client_id: An integer representing the client's ID (1 or 2)
    """
    global board, current_client
    print(f"Connection established with player '{CLIENT_SYMBOL[client_id]}, address {address}'")
    message = f"Greetings in Tic-Tac-Toe! You play by '{CLIENT_SYMBOL[client_id]}'. "

    if client_id == 1:
        message += "Waiting for the second player"
        current_client = client_socket
    else:
        message += "Please wait"

    client_socket.sendall(message.encode())

    while True:
        if len(clients) == 2:
            other_client_socket = [c for c in clients if c != client_socket][0]

            if current_client == client_socket:
                message = f"\nBoard:{board_to_string(board)}\nYour move. " \
                          f"Please type row and column (1-3) separated by space: "
                client_socket.sendall(message.encode())
                response = client_socket.recv(3)

                if not response:
                    break

                data = response.decode()

                print(f"Message from client {client_id}: {data}")
                updated_board = make_move(data, board, CLIENT_SYMBOL[client_id])

                # if the move was correct, update board
                if updated_board is not None:
                    board = updated_board

                    # check if the game is over
                    result = is_game_over(board)
                    if result is not None:
                        message = f"\n{result}\nFinal board:{board_to_string(board)}"
                        for c in clients:
                            c.sendall(message.encode())
                            c.close()
                        print(f"Game over. Connection closed with both players")
                        break

                    # swap current client
                    message = f"Board after your move:{board_to_string(board)}\nPlease wait"
                    client_socket.sendall(message.encode())
                    current_client = other_client_socket


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # reuse address if the OS hasn't released the port yet
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(2)

    print("Server is listening for incoming connections...")
    clients_connected = 0
    while clients_connected < 2:
        client_socket, address = server_socket.accept()
        clients_connected += 1
        clients.append(client_socket)

        client_thread = threading.Thread(target=handle_client, args=(client_socket, address, clients_connected))
        client_thread.start()

    print("\nServer has reached the maximum number of players.")


if __name__ == '__main__':
    main()
