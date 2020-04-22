from socket import AF_INET, socket, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
from argparse import ArgumentParser
# param is list of parameters

tutorial = ["If you ever want to quit, type 'quit' to exit.\n",
            "If you want to mine some Shitcoins from ECS153 Babychain, click the button 'mine' or type 'mine' in the terminal\n"
            "If you want to broadcast you balance, click the button 'balance' or type 'balance'\n",
            "If you want to broadcast your own public address, type 'addr'\n",
            "If you want to pay somebody, type 'pay <value> <public_addr>'\n"]
BUFSIZ = 4096
clients = {}
addresses = {}

def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Please type into your allias before doing any actions\n", "utf8"))
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
        parsed = msg.decode("utf-8").split("$")
        if len(parsed) > 1:
            broadcast(msg)
        elif msg != bytes("quit", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("quit", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
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
