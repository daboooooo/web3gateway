from time import time

import pytest

from web3gateway.config import load_config_json
from web3gateway.gateway_etherscanv2 import EtherScanV2


# 测试用的区块号 (以太坊主网 The Merge 区块)
TEST_BLOCK = 15537394


@pytest.fixture
async def etherscan():
    """创建 EtherScanV2 测试实例"""
    config = load_config_json(None)
    instance = await EtherScanV2.create(config)
    instance.set_chain_id(1)  # 使用以太坊主网
    return instance


@pytest.mark.asyncio
async def test_getblockreward(etherscan):
    """测试获取区块奖励"""
    result = await etherscan.block.getblockreward(TEST_BLOCK)
    assert isinstance(result, dict)
    assert 'blockNumber' in result
    assert 'blockMiner' in result
    assert 'blockReward' in result
    assert int(result['blockNumber']) == TEST_BLOCK


@pytest.mark.asyncio
async def test_getblockcountdown(etherscan):
    """测试获取区块倒计时"""
    # 获取当前区块号后加100作为目标区块
    latest_block = await etherscan.proxy.eth_block_number()
    target_block = int(latest_block, 16) + 100

    result = await etherscan.block.getblockcountdown(target_block)
    assert isinstance(result, dict)
    assert 'CurrentBlock' in result
    assert 'CountdownBlock' in result
    assert 'RemainingBlock' in result
    assert 'EstimateTimeInSec' in result
    assert int(result['CountdownBlock']) == target_block


@pytest.mark.asyncio
async def test_getblocknobytime(etherscan):
    """测试通过时间戳获取区块号"""
    # 使用当前时间戳
    current_timestamp = int(time()) - 3600

    # 测试获取"之前"的区块
    result_before = await etherscan.block.getblocknobytime(current_timestamp, "before")
    assert isinstance(result_before, str)
    assert result_before.isdigit()
    block_before = int(result_before)

    # 测试获取"之后"的区块
    result_after = await etherscan.block.getblocknobytime(current_timestamp, "after")
    assert isinstance(result_after, str)
    assert result_after.isdigit()
    block_after = int(result_after)

    # 确保"之后"的区块号大于等于"之前"的区块号
    assert block_after >= block_before


@pytest.mark.asyncio
async def test_getblocknobytime_specific_timestamp(etherscan):
    """测试使用特定时间戳获取区块号"""
    # 使用 The Merge 时间戳
    merge_timestamp = 1663224162  # 2022-09-15 06:42:42 UTC

    result = await etherscan.block.getblocknobytime(merge_timestamp, "before")
    assert isinstance(result, str)
    assert result.isdigit()
    block_number = int(result)
    # The Merge 发生在区块 15537393 左右
    assert 15537390 <= block_number <= 15537396
