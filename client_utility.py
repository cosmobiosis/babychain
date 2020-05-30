from backend.wallet import Wallet

BUFSIZ = 4096
wallet = Wallet()

def generate_transaction_broadcast(param):
    # param is list of parameters
    # first parameter is amount of transfer
    # second is receiver's public address string
    return wallet.pay(int(param[0]), param[1])

def check_balance(param):
    return wallet.check_others_balance(param[0])

def public_addr_broadcast(param):
    return wallet.user_addr

def mine(param):
    return wallet.mine()

def get_balance(param):
    return wallet.get_balance()

cmd = {
    "pay" : generate_transaction_broadcast,
    "addr": public_addr_broadcast,
    "balance": get_balance,
    "mine": mine,
    "check": check_balance
}