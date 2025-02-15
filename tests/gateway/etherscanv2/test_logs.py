import pytest

from web3gateway.config import load_config_json
from web3gateway.gateway_etherscanv2 import EtherScanV2


# 测试用的合约地址和区块范围
TEST_CONTRACT = "0xdac17f958d2ee523a2206206994597c13d831ec7"  # USDT合约
TEST_FROM_BLOCK = 17000000
TEST_TO_BLOCK = 17000100
TEST_TOPIC0 = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"  # Transfer事件


@pytest.fixture
async def etherscan():
    """创建 EtherScanV2 测试实例"""
    config = load_config_json(None)
    instance = await EtherScanV2.create(config)
    instance.set_chain_id(1)  # 使用以太坊主网
    return instance


@pytest.mark.asyncio
async def test_get_logs_by_address(etherscan):
    """测试通过地址获取日志"""
    result = await etherscan.logs.get_logs_by_address(
        address=TEST_CONTRACT,
        from_block=TEST_FROM_BLOCK,
        to_block=TEST_TO_BLOCK,
        page=1,
        offset=10
    )

    assert isinstance(result, list)
    if len(result) > 0:
        log = result[0]
        assert 'address' in log
        assert 'topics' in log
        assert 'data' in log
        assert 'blockNumber' in log
        assert 'timeStamp' in log


@pytest.mark.asyncio
async def test_get_logs_by_topic(etherscan):
    """测试通过主题获取日志"""
    result = await etherscan.logs.get_logs_by_topic(
        address=TEST_CONTRACT,
        from_block=TEST_FROM_BLOCK,
        to_block=TEST_TO_BLOCK,
        topic0=TEST_TOPIC0,
        topic0_1_opr="and",
        topic1="0x000000000000000000000000" + TEST_CONTRACT[2:],
        page=1,
        offset=10
    )

    assert isinstance(result, list)
    if len(result) > 0:
        log = result[0]
        assert 'address' in log
        assert 'topics' in log
        assert len(log['topics']) >= 2


@pytest.mark.asyncio
async def test_get_logs_by_address_filted_by_topic(etherscan):
    """测试通过地址和主题过滤获取日志"""
    result = await etherscan.logs.get_logs_by_address_filted_by_topic(
        from_block=TEST_FROM_BLOCK,
        to_block=TEST_TO_BLOCK,
        address=TEST_CONTRACT,
        topic0=TEST_TOPIC0,
        topic0_1_opr="and",
        topic1="0x000000000000000000000000" + TEST_CONTRACT[2:],
        page=1,
        offset=10
    )

    assert isinstance(result, list)
    if len(result) > 0:
        log = result[0]
        assert 'address' in log
        assert 'topics' in log
        assert 'blockNumber' in log
        assert 'transactionHash' in log
