import socket
from config import SERVER_ADDRESS, SERVER_PORT


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

    response = client_socket.recv(1024)
    print(f"{response.decode()}")

    while True:
        response = client_socket.recv(1024)
        if not response:
            print("The server has closed the connection.")
            break

        data = response.decode()
        print(f"{data}")

        message = ""

        if data.startswith("\nGame over"):
            break

        if not data.endswith("\nPlease wait"):
            while not message:
                message = input("Enter your move (type 'exit' for quit): ")

            if message == 'exit':
                break

            client_socket.sendall(message.encode())

    client_socket.close()


if __name__ == '__main__':
    main()
