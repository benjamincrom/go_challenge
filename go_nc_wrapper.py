import go
import socket

def go_server(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        print("Connection", addr)
        go_handler(client)

def go_handler(client):
    game = go.Game()
    result = game.board
    resp = str(result).encode('ascii')
    client.send(resp)
    while True:
        req = client.recv(100)
        if not req:
            break
        input_str = str(req)
        game.move(input_str)
        result = game.board
        resp = str(result).encode('ascii')
        client.send(resp)

go_server(('', 25000))
