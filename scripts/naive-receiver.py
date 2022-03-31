from brownie import NaiveReceiverLenderPool, FlashLoanReceiver, DamnValuableToken
from web3 import Web3
import time, sys
from scripts.helpful_scripts import get_accounts


def deploy():
    global deployer, user, pool, attacker, receiver, ETHER_IN_POOL, ETHER_IN_RECEIVER
    [deployer, user, attacker] = get_accounts(3)
    # Pool has 1M * 10**18 tokens
    ETHER_IN_POOL = Web3.toWei(1000, "ether")
    ETHER_IN_RECEIVER = Web3.toWei(10, "ether")

    # 开始部署
    pool = NaiveReceiverLenderPool.deploy({"from": deployer})
    deployer.transfer(pool, ETHER_IN_POOL).wait(1)

    assert pool.balance() == ETHER_IN_POOL
    assert pool.fixedFee() == Web3.toWei(1, "ether")

    receiver = FlashLoanReceiver.deploy(pool, {"from": user})
    user.transfer(receiver, ETHER_IN_RECEIVER).wait(1)
    assert receiver.balance() == ETHER_IN_RECEIVER


def attack():
    # 攻击代码写到这里
    return


def check():
    # 检测攻击是否完成： 不能继续借贷
    print("running func check..")
    try:
        assert receiver.balance() == 0
        assert pool.balance() == ETHER_IN_POOL + ETHER_IN_RECEIVER
        print("success!")
    except:
        time.sleep(1)
        print("Not pass yet ;(")

    return


def main():
    deploy()
    attack()
    check()
