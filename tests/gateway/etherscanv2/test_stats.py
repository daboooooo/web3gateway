from datetime import datetime, timedelta

import pytest

from web3gateway.config import load_config_json
from web3gateway.gateway_etherscanv2 import EtherScanV2


# 测试用的日期范围
END_DATE = datetime.now().strftime('%Y-%m-%d')
START_DATE = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')


@pytest.fixture
async def etherscan():
    """创建 EtherScanV2 测试实例"""
    config = load_config_json(None)
    instance = await EtherScanV2.create(config)
    instance.set_chain_id(1)  # 使用以太坊主网
    return instance


@pytest.mark.asyncio
async def test_ethsupply(etherscan):
    """测试获取以太币供应量"""
    result = await etherscan.stats.ethsupply()
    assert result is not None
    assert int(result) > 0


@pytest.mark.asyncio
async def test_ethsupply2(etherscan):
    """测试获取以太币供应量详情"""
    result = await etherscan.stats.ethsupply2()
    assert isinstance(result, dict)
    assert 'EthSupply' in result
    assert 'Eth2Staking' in result
    assert 'BurntFees' in result
    assert 'WithdrawnTotal' in result


@pytest.mark.asyncio
async def test_ethprice(etherscan):
    """测试获取以太币价格"""
    result = await etherscan.stats.ethprice()
    assert isinstance(result, dict)
    assert 'ethbtc' in result
    assert 'ethusd' in result
    assert float(result['ethusd']) > 0


@pytest.mark.asyncio
async def test_chainsize(etherscan):
    """测试获取区块链大小"""
    result = await etherscan.stats.chainsize(
        startdate=START_DATE,
        enddate=END_DATE
    )
    assert isinstance(result, list)
    if len(result) > 0:
        item = result[0]
        # "blockNumber":"7156164",
        # "chainTimeStamp":"2019-02-01",
        # "chainSize":"184726421279",
        # "clientType":"Geth",
        # "syncMode":"Default"
        assert 'blockNumber' in item
        assert 'chainTimeStamp' in item
        assert 'chainSize' in item
        assert 'clientType' in item
        assert 'syncMode' in item


@pytest.mark.asyncio
async def test_nodecount(etherscan):
    """测试获取节点数量"""
    result = await etherscan.stats.nodecount()
    assert isinstance(result, dict)
    assert 'TotalNodeCount' in result
    assert int(result['TotalNodeCount']) > 0


# @pytest.mark.asyncio
# async def test_dailytxnfee(etherscan):
#     """测试获取每日交易费用"""
#     try:
#         result = await etherscan.stats.dailytxnfee(
#             startdate=START_DATE,
#             enddate=END_DATE
#         )
#         assert isinstance(result, list)
#         if len(result) > 0:
#             item = result[0]
#             assert 'UTCDate' in item
#             assert 'transactionFee_Wei' in item
#     except Exception:
#         pytest.skip("PRO API feature")


# @pytest.mark.asyncio
# async def test_dailynewaddress(etherscan):
#     """测试获取每日新增地址数"""
#     try:
#         result = await etherscan.stats.dailynewaddress(
#             startdate=START_DATE,
#             enddate=END_DATE
#         )
#         assert isinstance(result, list)
#         if len(result) > 0:
#             item = result[0]
#             assert 'UTCDate' in item
#             assert 'newAddressCount' in item
#     except Exception:
#         pytest.skip("PRO API feature")


# @pytest.mark.asyncio
# async def test_dailynetutilization(etherscan):
#     """测试获取每日网络使用率"""
#     try:
#         result = await etherscan.stats.dailynetutilization(
#             startdate=START_DATE,
#             enddate=END_DATE
#         )
#         assert isinstance(result, list)
#         if len(result) > 0:
#             item = result[0]
#             assert 'UTCDate' in item
#             assert 'networkUtilization' in item
#     except Exception:
#         pytest.skip("PRO API feature")

# # PRO API features - 简单测试
# @pytest.mark.asyncio
# @pytest.mark.parametrize("method", [
#     'dailyavghashrate',
#     'dailytx',
#     'dailyavgnetdifficulty',
#     'ethdailymarketcap',
#     'ethdailyprice'
# ])
# async def test_pro_features(etherscan, method):
#     """测试PRO API特性"""
#     try:
#         result = await getattr(etherscan.stats, method)(
#             startdate=START_DATE,
#             enddate=END_DATE
#         )
#         assert isinstance(result, (dict, list))
#     except Exception:
#         pytest.skip(f"PRO API feature: {method}")
