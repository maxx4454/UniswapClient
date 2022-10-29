from src.const import w3, ADDR, N, START_ADDR
from client import Bot, Chain


def main():
    block_num_old = w3.eth.get_block_number()
    chains = [(Chain(ADDR[(len(ADDR) // N) * i:(len(ADDR) // N) * (i + 1)], START_ADDR[i])) for i in range(N)]
    bots = [Bot(chain) for chain in chains]

    while True:
        block_num_new = w3.eth.get_block_number()
        if block_num_old != block_num_new:
            print('new block, processing')
            for bot in bots:
                bot.next()
            block_num_old = block_num_new


if __name__ == "__main__":
    main()
