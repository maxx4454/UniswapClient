from resources.const import *


def tg_notify(bot_message):
    send_text = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + CHAT_ID + \
                '&parse_mode=HTML&text=' + bot_message

    response = requests.post(send_text)
    print('tg sent')
    return response


def read_privates(file_name):
    with open(file_name, 'r') as f:
        ans = f.read().split()
        while '' in ans:
            ans.remove('')
        while ' ' in ans:
            ans.remove(' ')

    addr = []
    for private in ans:
        account = web3.eth.account.from_key(private)
        public = account.address
        addr.append((public, private))

    return addr


def split_chains(n):
    chains = []
    addr = read_privates("settings/privates.txt")
    part_l = len(addr) // n
    for i in range(n):
        chains.append(Chain(addr[part_l * i:part_l * (i + 1)]))

    return chains
