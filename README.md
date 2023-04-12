# Tic Tac Toe Over Sockets
This is a simple implementation of a Tic Tac Toe game played over sockets. It allows two players to play the classic game in a turn-based manner, connecting to a server using a client application. The server handles game logic, board updates, and player moves.

## Installation
Clone the repository:
```
git clone https://github.com/aintlikeu/tic_tac_toe_over_sockets.git
```

## Usage
1. Start the server:
```
python server.py
```
The server will listen for incoming connections on localhost and port 12345.

2. Start the client application in two separate terminals:
```
python client.py
```
Each client represents a player. The first player will be assigned the symbol 'X', and the second player will be assigned the symbol 'O'.

Follow the on-screen instructions to play the game. Players take turns entering their moves in the form of row and column numbers (1-3), separated by a space.

The game will continue until a player wins, or there are no valid moves left, resulting in a draw.

## License
This project is released under the [MIT License](https://opensource.org/licenses/MIT).