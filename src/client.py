from const import SEND_COMMISSION, SWAP_COMMISSION, w3, SKIPS
from web3utils import sell, buy, send
import random


# TODO: что здесь творится??
class Chain:
    def __init__(self, adrs, start_adr, skips=SKIPS):
        a = [True for _ in range(len(adrs) - skips + 1)]
        for i in range(skips):
            a.append(False)
        random.shuffle(a)
        a[0] = True
        random.shuffle(adrs)
        adrs.insert(0, start_adr)
        self.public = [w3.toChecksumAddress(el[0]) for el in adrs]
        self.private = [el[1] for el in adrs]
        self.active = a
        self.limit = [(0.05 * 10 ** 18) * (i + 1) for i in range(len(adrs))]

        # TODO: ???
        self.commision = [SEND_COMMISSION + SWAP_COMMISSION if self.active[i] else SEND_COMMISSION for i in
                          range(len(adrs))]


class Bot:
    def __init__(self, chain):
        self.chain = chain
        self.index = 0

    @property
    def public(self):
        return self.chain.public[self.index]

    @property
    def private(self):
        return self.chain.private[self.index]

    @property
    def commission(self):
        return self.chain.commision[self.index]

    @property
    def active(self):
        return self.chain.active[self.index]

    def next(self):
        if self.get_available_balance() > 0:
            print('balance bigger than 0')
            if self.active:
                self.swap_and_send_rest()
            else:
                self.sell_from_old_account()
            self.index += 1

    def get_available_balance(self, chain_index=None):
        if chain_index is None:
            chain_index = self.index
        return w3.eth.get_available_balance(self.chain.public[chain_index]) - self.chain.commision[chain_index]

    def swap_and_send_rest(self):
        # do random split
        buy_amount, send_amount = self.split()
        # buy for money
        buy(account=self.chain.public[self.index], amount_eth=buy_amount, private=self.private)
        print('swapped')
        # send the rest to the next account
        to = self.find_next_account_index()
        send(send_amount, nonce_mode='increment')
        print('sent')

    def find_next_account_index(self):
        to_index = self.index + 1
        while not self.chain.active[to_index]:
            to_index += 1
        return to_index

    def find_first_buyer_with_tokens(self):
        to_index = self.index + 1
        while not self.chain.active[to_index]:
            to_index += 1
        return to_index

    def split(self):
        balance = self.get_available_balance()
        buy_amount = random.randint(10 ** 15, min(balance, self.chain.limit[self.index]))

        # округление buy_amount до 0.001 eth
        shit = buy_amount % 10 ** 15
        buy_amount -= shit

        send_amount = balance - buy_amount
        return buy_amount, send_amount

    def sell_from_old_account(self):
        account = self.find_first_buyer_with_tokens()
        sell(account)
        # send the rest to the next account
        send()
