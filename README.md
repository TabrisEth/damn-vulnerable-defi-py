# damn-vulnerable-defi-py
DeFi 协议带来了在闪贷等传统金融中无法实现的新颖创新。在DeFi协议开发上同样需要考虑的新攻防方法。其中OpenZeppelin 发布了他们的[Damn Vulnerable DeFi CTF](https://www.damnvulnerabledefi.xyz/)。

这套题很简练和有趣，这是开始 DeFi 或 ETH 开发的好方法。与其他 CTF 不同，一切都在本地节点上运行，因此无需浪费时间进行设置，例如管理私钥、获取 testnet ether、将代码复制到本地机器等。试试看吧！您可以在此 GitHub 存储库中查看我针对所有挑战的解决方案，并且与官方使用js答解不同，我使用python、brownie重新编写整套题。

更详细的介绍可以查看：[文档](https://mirror.xyz/tabris.eth/zEB0CH484jGv6wBVO1vs3e3FqFkTESGh1-F4l-LEUtU)

# 环境准备

## 安装brownie、web3py

```bash
pipx install eth-brownie
```

## 克隆git，并且初始化brownie

```bash
git clone TabrisEth/damn-vulnerable-defi-py
cd damn-vulnerable-defi-py
brownie init
```

## 目录解释

* contracts 试题合约目录（无需改动这里）

* scripts 试题brownie脚本目录

编辑改动所有脚本中的attack函数，例如
```python
def attack():
    # 攻击代码写到这里
    token.transfer(pool, 1, {"from": attacker}).wait(1)
    return
```
## 进行攻击&运行
运行：
```bash
brownie run scripts/unstoppable.py 
```
