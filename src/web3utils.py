from const import w3, TOKEN_CONTRACT, TOKEN, GAS, WETH, ROUTER_CONTRACT
import time


def send_tx(tx, private):
    signed_tx = w3.eth.account.sign_transaction(tx, private)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(f"tx signed: {tx_hash}")


def get_nonce(account, nonce_mode='non_increment'):
    if nonce_mode == 'increment':
        return w3.eth.getTransactionCount(account) + 1
    elif nonce_mode == "non_increment":
        return w3.eth.getTransactionCount(account)
    else:
        print('nonce mode troubles')


def tx_params(nonce, from_, to, gas_limit, gas_price, value):
    return {
        "nonce": nonce,
        "from": from_,
        "to": to,
        "gas": gas_limit,
        "gasPrice": gas_price,
        "value": value
    }


def send(to, from_, amount, private, nonce_mode='increment'):
    try:
        nonce = get_nonce(account=from_, nonce_mode=nonce_mode)
        tx = tx_params(from_=from_, nonce=nonce, to=to, value=int(amount), gas_limit=21_000, gas_price=GAS)
        send_tx(tx, private)
    except Exception as e:
        print(e)


# TODO: хз работает ли это вообще
def get_token_balance(account):
    return TOKEN_CONTRACT.functions.balance(account)


def sell(account, amount_token, private, nonce_mode='increment'):
    try:
        print(f"sell: {account}")
        nonce = get_nonce(account, nonce_mode=nonce_mode)

        # TODO: add amount of swap добавил как ущерб посмотрет как функция выглядит
        tx_to_swap = ROUTER_CONTRACT.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
            1, [TOKEN, WETH], account, amount_token, int(time.time()) + 500_000
        ).buildTransaction(
            tx_params(from_=account, nonce=nonce, to=ROUTER_CONTRACT, value=0, gas_limit=250_000, gas_price=GAS)
        )

        send_tx(tx_to_swap, private)
    except Exception as e:
        print(e)


# TODO: шафлить метод вызываемый в контракет чтобы в эфирскане по-разному выглядело
def buy(account, amount_eth, private, nonce_mode='increment'):
    try:
        print(f"buy: {account}")
        nonce = get_nonce(account, nonce_mode=nonce_mode)

        tx_to_swap = ROUTER_CONTRACT.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
            1, [WETH, TOKEN], account, int(time.time()) + 500_000
        ).buildTransaction(
            tx_params(from_=account, nonce=nonce, to=ROUTER_CONTRACT, value=int(amount_eth), gas_limit=250_000,
                      gas_price=GAS)
        )

        send_tx(tx_to_swap, private)
    except Exception as e:
        print(e)
