# param is list of parameters

def quitchat(client, name, param):
    client.send(bytes("quit", "utf8"))
    client.close()
    del clients[client]
    broadcast(bytes("%s has left the chat." % name, "utf8"))
    return

def balance(client, name, param):
    return

def mine(client, name, param):
    return

def pay(client, name, param):
    client.send(bytes("Me pay\n", "utf8"))
    val_str = param[0]
    val = int(val_str)
    receiver_public_address = param[1]

    msg = "User " + name + " with public_address\n" + "\npay $" + val_str \
          + " To user with public address\n" + receiver_public_address+'\n'
    broadcast(bytes(msg, "utf8"), name + ": ")
    return

def nodes(client, name, param):
    return

cmd = {"quit" : quitchat,
       "balance" : balance,
       "pay": pay,
       "nodes": nodes,
       "mine": mine}

tutorial = ["If you ever want to quit, type 'quit' to exit.\n",
            "If you want to mine some Shitcoins from ECS153 Babychain, type 'mine'\n"
            "If you want to check you balance, type 'balance' to check it\n",
            "If you want to check people's public keys registered in this net, type 'nodes'\n",
            "If you want to pay somebody, type 'pay <value> <public_key>'\n"]

BUFSIZ = 1024
clients = {}
addresses = {}

def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)