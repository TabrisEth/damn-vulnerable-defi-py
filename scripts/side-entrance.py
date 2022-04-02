from brownie import SideEntranceLenderPool
from web3 import Web3
import time
from scripts.helpful_scripts import get_accounts


def deploy():
    global deployer, attacker, ETHER_IN_POOL, pool, attackerInitialEthBalance
    [deployer, attacker] = get_accounts(2)
    # Pool has 1M * 10**18 tokens
    ETHER_IN_POOL = Web3.toWei(1000, "ether")

    # 开始部署
    pool = SideEntranceLenderPool.deploy({"from": deployer})
    pool.deposit({"from": deployer, "value": ETHER_IN_POOL}).wait(1)
    attackerInitialEthBalance = attacker.balance()

    assert pool.balance() == ETHER_IN_POOL


def attack():
    # 攻击代码写到这里
    print("running func attack..")
    return


def check():
    # 检测攻击是否完成： 不能继续借贷
    print("running func check..")
    try:
        assert pool.balance() == 0
        assert attacker.balance() > attackerInitialEthBalance
        print("success!")
    except:
        time.sleep(1)
        print("Not pass yet ;(")

    return


def main():
    deploy()
    attack()
    check()
