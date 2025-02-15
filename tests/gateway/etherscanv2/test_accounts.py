import pytest

from web3gateway.config import load_config_json
from web3gateway.gateway_etherscanv2 import EtherScanV2


# 测试用的以太坊地址
TEST_ADDRESS = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"  # Binance hot wallet
TEST_CONTRACT = "0xdac17f958d2ee523a2206206994597c13d831ec7"  # USDT contract
TEST_BLOCK = 5540000


@pytest.fixture
async def etherscan():
    """创建 EtherScanV2 测试实例"""
    config = load_config_json(None)
    instance = await EtherScanV2.create(config)
    instance.set_chain_id(1)  # 使用以太坊主网
    return instance


@pytest.mark.asyncio
async def test_balance(etherscan):
    """测试获取账户余额"""
    result = await etherscan.account.balance(TEST_ADDRESS)
    assert result is not None
    assert int(result) >= 0


@pytest.mark.asyncio
async def test_balancemulti(etherscan):
    """测试批量获取账户余额"""
    addresses = [TEST_ADDRESS, "0x1f9090aaE28b8a3dCeaDf281B0F12828e676c326"]
    result = await etherscan.account.balancemulti(",".join(addresses))
    assert isinstance(result, list)
    assert len(result) == 2
    for balance in result:
        assert int(balance['balance']) >= 0


@pytest.mark.asyncio
async def test_txlist(etherscan):
    """测试获取账户交易列表"""
    result = await etherscan.account.txlist(
        TEST_ADDRESS,
        startblock=TEST_BLOCK,
        endblock=TEST_BLOCK + 10000
    )
    assert isinstance(result, list)
    if len(result) > 0:
        tx = result[0]
        assert 'from' in tx
        assert 'to' in tx
        assert 'value' in tx


@pytest.mark.asyncio
async def test_tokentx(etherscan):
    """测试获取代币交易列表"""
    try:
        result = await etherscan.account.tokentx(
            TEST_ADDRESS,
            TEST_CONTRACT,
            startblock=TEST_BLOCK,
            endblock=TEST_BLOCK + 10000
        )
    except ValueError:
        return

    assert isinstance(result, list)
    if len(result) > 0:
        tx = result[0]
        assert 'from' in tx
        assert 'to' in tx
        assert 'tokenName' in tx


@pytest.mark.asyncio
async def test_getminedblocks(etherscan):
    """测试获取账户挖矿区块列表"""
    result = await etherscan.account.getminedblocks(
        "0x4bb96091ee9d802ed039c4d1a5f6216f90f81b01"  # 一个矿工地址
    )
    assert isinstance(result, list)
    if len(result) > 0:
        block = result[0]
        assert 'blockNumber' in block
        assert 'blockReward' in block


# @pytest.mark.asyncio
# async def test_balancehistory(etherscan):
#     """测试获取历史余额"""
#     result = await etherscan.account.balancehistory(TEST_ADDRESS, TEST_BLOCK)
#     assert result is not None
#     assert int(result) >= 0


# @pytest.mark.asyncio
# async def test_txsbeaconwithdrawal(etherscan):
#     """测试获取信标链提款记录"""
#     result = await etherscan.account.txsbeaconwithdrawal(
#         TEST_ADDRESS,
#         startblock=TEST_BLOCK,
#         endblock=TEST_BLOCK + 10000
#     )
#     assert isinstance(result, list)
