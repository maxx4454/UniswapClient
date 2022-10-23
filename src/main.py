from resources.const import web3
from client import Bot, split_chains
from settings.config import N


def main():
    block_num_old = web3.eth.get_block_number()
    chains = split_chains(N)
    bots = []
    for chain in chains:
        bots.append(Bot(chain))

    while True:
        block_num_new = web3.eth.get_block_number()
        if block_num_old != block_num_new:
            for bot in bots:
                bot.next()
            block_num_old = block_num_new


if __name__ == "__main__":
    main()
