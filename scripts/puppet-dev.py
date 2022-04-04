# still not finish yet ;(
from web3 import Web3
from brownie import web3
from brownie.project import compiler
import time, json
from scripts.helpful_scripts import get_accounts


def deploy():
    global deployer, attacker, TOKENS_IN_POOL, token, governance, pool
    [
        deployer,
        attacker,
    ] = get_accounts(2)
    # Pool has 1M * 10**18 tokens
    UNISWAP_INITIAL_TOKEN_RESERVE = Web3.toWei(10, "ether")
    UNISWAP_INITIAL_ETH_RESERVE = Web3.toWei(10, "ether")
    POOL_INITIAL_TOKEN_BALANCE = Web3.toWei(1000, "ether")
    ATTACKER_INITAL_TOKEN_BALANCE = Web3.toWei(100, "ether")

    # 开始部署
    with open("build-uniswap-v1/UniswapV1Exchange.json", "r") as f:
        UniswapV1Exchange = compiler.compile_from_input_json(json.load(f))

    token = DamnValuableToken.deploy({"from": deployer})
    exchangeTemplate = UniswapV1Exchange.deploy({"from": deployer})
    return


def attack():
    # 攻击代码写到这里
    print("running func attack..")
    return


def check():
    # 检测攻击是否完成
    print("running func check..")
    try:
        print("success!")
    except:
        time.sleep(1)
        print("Not pass yet ;(")

    return


def main():
    deploy()
    attack()
    check()
