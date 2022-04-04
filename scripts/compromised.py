from brownie import Exchange, DamnValuableNFT, TrustfulOracle, TrustfulOracleInitializer
from web3 import Web3
from brownie import web3
from brownie.network.state import Chain
import time
from scripts.helpful_scripts import get_accounts


def deploy():
    global deployer, attacker, token, exchange
    sources = [
        "0xA73209FB1a42495120166736362A1DfA9F95A105",
        "0xe92401A4d3af5E446d93D11EEc806b1462b39D15",
        "0x81A5D6E50C214044bE44cA0CB057fe119097850c",
    ]
    [
        deployer,
        attacker,
    ] = get_accounts(2)
    # Pool has 1M * 10**18 tokens
    EXCHANGE_INITIAL_ETH_BALANCE = Web3.toWei(10000, "ether")
    INITIAL_NFT_PRICE = Web3.toWei(999, "ether")

    # 开始部署
    deployer.transfer(sources[0], "5 ether").wait(1)
    deployer.transfer(sources[1], "5 ether").wait(1)
    deployer.transfer(sources[2], "5 ether").wait(1)

    oracle = TrustfulOracle.at(
        TrustfulOracleInitializer.deploy(
            sources,
            ["DVNFT", "DVNFT", "DVNFT"],
            [INITIAL_NFT_PRICE, INITIAL_NFT_PRICE, INITIAL_NFT_PRICE],
            {"from": deployer},
        ).oracle()
    )
    exchange = Exchange.deploy(
        oracle, {"from": deployer, "value": EXCHANGE_INITIAL_ETH_BALANCE}
    )
    token = DamnValuableNFT.at(exchange.token())
    initialAttackerBalance = attacker.balance()

    return


def attack():
    # 攻击代码写到这里
    print("running func attack..")
    return


def check():
    # 检测攻击是否完成
    print("running func check..")
    try:
        assert exchange.balance() == 0
        print("success!")
    except:
        time.sleep(1)
        print("Not pass yet ;(")

    return


def main():
    deploy()
    attack()
    check()
