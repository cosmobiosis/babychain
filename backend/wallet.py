from backend.chain import *
import copy

class Wallet:
    def __init__(self):
        self.block_chain = Blockchain()

        random_gen = Crypto.Random.new().read
        # Static attributes of keys generated
        self._private_key = RSA.generate(1024, random_gen)
        self._public_key = self._private_key.publickey()
        self._signer = PKCS1_v1_5.new(self._private_key)
        self.user_addr = binascii.hexlify(self._public_key.exportKey(format='DER')).decode('utf-8')

    def receive_broadcast(self, message):
        parsed = message.split('$')
        if len(parsed) == 2:
            return self.verify_new_block(message)
        if len(parsed) == 3:
            return self.verify_transaction(message)
        return None

    def mine(self):
        last_block = self.block_chain.blocks[-1]
        last_hash = self.block_chain.hash_digest(last_block)
        nonce = self.block_chain.proof_of_work(last_hash)
        block = self.block_chain.add_block(nonce, last_hash, self.user_addr)
        nonce = block["nonce"]
        """
        Only Pass UTF-8 Encoded String
        Prepare for two parameters: miner_addr, nonce
        mining_broadcast_message = "string + '$' + string " as payload
        """
        mining_broadcast_message = self.user_addr + "$" + str(nonce)
        return mining_broadcast_message

    def pay(self, value, receiver_addr):
        balance = self.get_balance()
        if balance < value:
            raise ValueError("Insufficient Balance")
        # Has to follow the sorted key order
        transaction = {'receiver': receiver_addr, 'sender': self.user_addr, 'value': value}
        txn_message = json.dumps(transaction, sort_keys=True)
        signature = self._signer.sign(SHA.new(txn_message.encode()))
        """
        Only Pass UTF-8 Encoded String
        Prepare for three parameters: transaction message, sender public key, signature
        transaction_broadcast_message = "string + '$' + string + '$' + string" as payload
        """
        sender_public_key_string = binascii.hexlify(self._public_key.exportKey(format='DER')).decode('utf-8')
        signature_string = binascii.hexlify(signature).decode('utf-8')
        transaction_broadcast_message = txn_message+"$"+sender_public_key_string+"$"+signature_string
        return transaction_broadcast_message

    def verify_new_block(self, mining_broadcast_message):
        parsed = mining_broadcast_message.split('$')
        miner_addr = parsed[0]
        nonce = int(parsed[1])

        if miner_addr == self.user_addr or self.block_chain.verify_new_block(miner_addr, nonce):
            # Validate his own block
            msg = "a node has verified new block"
            return msg

        return "This block is invalid!"

    def verify_transaction(self,transaction_broadcast_message):
        # Parsed the broadcast message
        parsed = transaction_broadcast_message.split('$')
        txn_message = parsed[0]
        sender_public_key_string = parsed[1]
        signature_string = parsed[2]
        if self.block_chain.verify_transaction_signature(txn_message, sender_public_key_string, signature_string):
            msg = "a node has verified new transaction"
            return msg

        return "This transaction is invalid!"

    def get_balance(self):
        balance = 0
        for block in self.block_chain.blocks:
            if block['miner'] == self.user_addr:
                balance += REWARD
            transactions = block['txn']
            for each_txn in transactions:
                if each_txn['sender'] == self.user_addr:
                    balance -= each_txn['value']
                if each_txn['receiver'] == self.user_addr:
                    balance += each_txn['value']
        if balance < 0:
            raise ValueError("Balance Smaller than 0")
        return balance

