from brownie import DamnValuableTokenSnapshot, SelfiePool, SimpleGovernance
from web3 import Web3
from brownie import web3
from brownie.network.state import Chain
import time
from scripts.helpful_scripts import get_accounts


def deploy():
    global deployer, attacker, TOKENS_IN_POOL, token, governance, pool
    [
        deployer,
        attacker,
    ] = get_accounts(2)
    # Pool has 1M * 10**18 tokens
    TOKEN_INITIAL_SUPPLY = Web3.toWei(2000000, "ether")
    TOKENS_IN_POOL = Web3.toWei(1500000, "ether")

    # 开始部署
    token = DamnValuableTokenSnapshot.deploy(TOKEN_INITIAL_SUPPLY, {"from": deployer})
    governance = SimpleGovernance.deploy(token, {"from": deployer})
    pool = SelfiePool.deploy(token, governance, {"from": deployer})

    token.transfer(pool, TOKENS_IN_POOL, {"from": deployer}).wait(1)
    assert token.balanceOf(pool) == TOKENS_IN_POOL

    return


def attack():
    # 攻击代码写到这里
    print("running func attack..")
    return


def check():
    # 检测攻击是否完成
    print("running func check..")
    try:
        assert token.balanceOf(attacker) == TOKENS_IN_POOL
        assert token.balanceOf(pool) == 0
        print("success!")
    except:
        time.sleep(1)
        print("Not pass yet ;(")

    return


def main():
    deploy()
    attack()
    check()
