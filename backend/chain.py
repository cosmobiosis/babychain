from hashlib import sha256
import json
from collections import OrderedDict

import binascii
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

Difficulty = 2
REWARD = 50

class Blockchain:

    def __init__(self):
        self.blocks = []
        """
        txn is referred to Current Block Transactions
        Will reset after new block added to the blocks
        """
        self.transactions = []
        empty_string = ""
        genesis_hash = sha256(empty_string.encode()).hexdigest()
        self.add_block(0, genesis_hash, '')


    def add_block(self, nonce, previous_hash, miner):

        block = {'miner' : miner,
                'index': len(self.blocks),
                'txn': self.transactions,
                'prehash': previous_hash,
                'nonce' : nonce,
                 }

        self.transactions = [] # reset the transactions
        self.blocks.append(block)
        return block

    def hash_digest(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return sha256(block_string).hexdigest()

    def proof_of_work(self, previous_hash):
        # Get the proof of work by bruteforcing the hash
        nonce = 0
        prefix = '0' * Difficulty
        while True:
            bruteforce_candidate = sha256((str(self.transactions)+str(previous_hash)+str(nonce)).encode()).hexdigest()
            # default encoding to utf-8
            if bruteforce_candidate.startswith(prefix):
                # print("Find the hash using ", nonce, " iterations")
                return nonce
            nonce += 1

    def verify_new_block(self, miner_addr, nonce):
        last_block = self.blocks[-1]
        last_hash = self.hash_digest(last_block)
        prefix = '0' * Difficulty
        to_verify = sha256((str(self.transactions) + str(last_hash) + str(nonce)).encode()).hexdigest()

        if to_verify.startswith(prefix):
            self.add_block(nonce, last_hash, miner_addr)
            return True
        else:
            raise ValueError("New Block Invalid")


    def verify_transaction_signature(self, txn_message, sender_public_key_string, signature_string):
        # transaction = { 'sender': self.user_addr, 'receiver': receiver, 'value': value }
        # Restore transaction, sender_public_key, signature from UTF-8 encoded string
        transaction = json.loads(txn_message)
        sender_public_key = RSA.import_key(binascii.unhexlify(sender_public_key_string))
        signature = binascii.unhexlify(signature_string)

        h = SHA.new(txn_message.encode())
        verifier = PKCS1_v1_5.new(sender_public_key)
        if verifier.verify(h, signature):
            self.transactions.append(transaction)
            return True
        else:
            raise ValueError("Authentication Failed")
