from brownie import DamnValuableToken, TrusterLenderPool, AttackTruster
from web3 import Web3
import time
from scripts.helpful_scripts import get_accounts


def deploy():
    global deployer, attacker, token, pool, TOKENS_IN_POOL
    [deployer, attacker] = get_accounts(2)
    # Pool has 1M * 10**18 tokens
    TOKENS_IN_POOL = Web3.toWei(1000000, "ether")

    # 开始部署
    token = DamnValuableToken.deploy({"from": deployer})
    pool = TrusterLenderPool.deploy(token, {"from": deployer})
    token.transfer(pool, TOKENS_IN_POOL, {"from": deployer}).wait(1)

    assert token.balanceOf(pool) == TOKENS_IN_POOL
    assert token.balanceOf(attacker) == 0


def attack():
    # 攻击代码写到这里
    attack_contract = AttackTruster.deploy({"from": attacker})
    attack_contract.attack(token, pool, attacker).wait(1)
    return


def check():
    # 检测攻击是否完成： 不能继续借贷
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
