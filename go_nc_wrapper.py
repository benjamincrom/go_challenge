import go
import socket
from threading import Thread

def go_server(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        print("Connection", addr)
        result = Thread(target=go_handler, args=(client,)).start()

def go_handler(client):
    game = go.Game()
    result = game.board
    resp = str(result).encode('ascii')
    client.send(resp)
    while True:
        req = client.recv(100)
        if not req:
            break
        result = game.move(str(req))
        resp = str(result).encode('ascii')
        client.send(resp)

go_server(('', 25000))
