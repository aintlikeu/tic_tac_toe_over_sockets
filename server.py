import socket
import threading
from services import make_move

CLIENT_SYMBOL = {1: 'X', 2: 'O'}

clients = []
current_client = None
current_move = 1
board = [['_'] * 3 for _ in range(3)]


def handle_client(client_socket, address, client_id):
    global board, current_client, current_move
    print(f"Connection established with player '{CLIENT_SYMBOL[client_id]}'")
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
                message = f"\nBoard: {board}\nMove #{current_move}. " \
                          f"Please type row and column (1-3) separated by space: "
                client_socket.sendall(message.encode())
                response = client_socket.recv(3)

                if not response:
                    break

                data = response.decode()

                print(f"Message from client {client_id}: {data}")
                updated_board = make_move(data, board, CLIENT_SYMBOL[client_id])

                if updated_board is not None:
                    board = updated_board
                    current_client = other_client_socket
                    current_move += 1
                    message = "\nPlease wait\n"
                else:
                    message = f"\nBoard: {board}\n" \
                              f"Invalid input. Retry\n"

                client_socket.sendall(message.encode())

                if current_move > 9:
                    message = f"No more moves. Draw"
                    client_socket.sendall(message.encode)
                    other_client_socket.sendall(message.encode)
                    break

    print(f"Connection closed with player '{CLIENT_SYMBOL[client_id]}'")
    client_socket.close()


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

    print("Server has reached the maximum number of players.")


if __name__ == '__main__':
    main()
