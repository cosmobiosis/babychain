from socket import AF_INET, socket, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
from argparse import ArgumentParser
from server_utility import *

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Please Register Your node by typing into your allias\n", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s!\n' % name
    client.send(bytes(welcome, "utf8"))
    for each in tutorial:
        client.send(bytes(each, "utf8"))
    msg = "%s has joined the chat!\n" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        msg = msg.decode("utf-8")
        parsed = msg.split()

        if parsed[0] not in cmd:
            broadcast(bytes(msg, "utf8"), name + ": ")
        else:
            param = []
            for i in range(1, len(parsed)):
                param.append(parsed[i])
            cmd[parsed[0]](client, name, param)
            if parsed[0] == "quit":
                break


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=23333, type=int, help='port to listen on')
    parser.add_argument('-ip', default='127.0.0.1', type=str)
    args = parser.parse_args()
    PORT = args.port
    HOST = args.ip
    ADDR = (HOST, PORT)

    SERVER = socket(AF_INET, SOCK_STREAM)
    SERVER.bind(ADDR)

    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()