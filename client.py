import socket


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    response = client_socket.recv(1024)
    print(f"{response.decode()}")

    while True:
        response = client_socket.recv(1024)

        if not response:
            break

        data = response.decode()
        print(f"{data}")

        message = ""
        if not data.startswith("\nPlease wait\n"):
            while not message:
                message = input("Enter your move (type 'exit' for quit): ")

            if message == 'exit':
                break

            client_socket.sendall(message.encode())

    client_socket.close()


if __name__ == '__main__':
    main()
