import copy
import json

class Network:
    def __init__(self):
        self.user_nodes = {}

    def add_user_node(self, wallet):
        useraddr = wallet.user_addr
        self.user_nodes[useraddr] = wallet

    def broadcast(self, message):
        for addr in self.user_nodes:
            wallet = self.user_nodes[addr]
            wallet.receive_broadcast(message)