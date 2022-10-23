from utils import *
from resources.const import *


def split_chains(n):
    chains = []
    addr = read_privates("../settings/privates.txt")
    part_l = len(addr) // n
    for i in range(n):
        chains.append(Chain(addr[part_l * i:part_l * (i + 1)]))

    return chains


class Chain:
    def __init__(self, adrs, skips=2):
        a = [True for _ in range(len(adrs) - skips)]
        for i in range(skips):
            a.append(False)
        random.shuffle(a)
        self.public = [web3.toChecksumAddress(el[0]) for el in adrs]
        self.private = [el[1] for el in adrs]
        self.incl = a
        self.limit = [(0.05 * 10 ** 18) * (i + 1) for i in range(len(adrs))]


class Bot:
    def __init__(self, chain):
        self.chain = chain
        self.step = 0

    def next(self):
        incl = self.chain.incl[self.step]
        if incl:
            # do random split
            h_1, h_2 = self.split()
            # buy for money
            self.swap_exact_amount(h_1)
            # send the rest to the next account
            self.send(h_2)
        else:
            self.send(self.get_balance())
        self.step += 1

    def get_balance(self):
        return web3.eth.get_balance(self.chain.public[self.step]) - 2 * COMMISSION

    def split(self):
        balance = self.get_balance()
        if balance > 0:
            h_1 = random.randint(1, min(balance, self.chain.limit[self.step]))
            h_2 = balance - h_1
            return h_1, h_2
        else:
            return -1, -1

    def swap_exact_amount(self, amount):
        try:
            tg_notify("started the swap")
            # get the nonce
            nonce = web3.eth.getTransactionCount(self.chain.public[self.step])
            start = time.time()
            # amount_in_wei = web3.toWei(amount, "ether")

            token_from = web3.toChecksumAddress(WETH_GOERLI)
            token_to = web3.toChecksumAddress(TOKEN)
            print("building the tx")

            tx_to_swap = ROUTER_CONTRACT.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
                1, [token_from, token_to], self.chain.public[self.step], int(start) + 500_000
            ).buildTransaction({
                "nonce": nonce,
                "from": self.chain.public[self.step],
                "gas": 250_000,
                "gasPrice": int(web3.eth.gas_price * 1.2),
                "value": int(amount)
            })

            signed_tx = web3.eth.account.signTransaction(tx_to_swap, self.chain.private[self.step])
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            print(f"tx signed: {tx_hash}")
        except Exception as e:
            print(e)

    def send(self, amount):
        try:
            i = self.step + 1
            while not self.chain.incl[i]:
                i += 1

            nonce = web3.eth.getTransactionCount(self.chain.public[self.step])
            tx = {
                'nonce': nonce,
                'to': self.chain.public[i],
                'value': int(amount),
                'gas': 21000,
                'gasPrice': int(web3.eth.gas_price * 1.2)
            }

            signed_tx = web3.eth.account.sign_transaction(tx, self.chain.private[self.step])
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            print(f"tx signed: {tx_hash}")
        except Exception as e:
            print(e)
