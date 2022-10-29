import json
import web3


# TODO: должен возвращать дикт ?
def load_cfg_dict():
    return json.loads('config.json')


def return_config_params(*args):
    d = load_cfg_dict()
    return tuple([d[x] for x in args])


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
