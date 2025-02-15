import pytest

from web3gateway.config import load_config_json
from web3gateway.gateway_etherscanv2 import EtherScanV2


# 测试用的交易哈希
TEST_SUCCESS_TX = "0x29f2df8ce6a4cef0b6d49942a9f4a544404773df67c3c7b5735a86b0ce87764f"  # 成功的交易
TEST_FAILED_TX = "0x15f8e5ea1079d9a0bb04a4c58ae5fe7654b5b2b4463375ff7ffb490aa0032f3a"   # 失败的交易


@pytest.fixture
async def etherscan():
    """创建 EtherScanV2 测试实例"""
    config = load_config_json(None)
    instance = await EtherScanV2.create(config)
    instance.set_chain_id(1)  # 使用以太坊主网
    return instance


@pytest.mark.asyncio
async def test_getstatus_success(etherscan):
    """测试获取成功交易的状态"""
    result = await etherscan.transaction.getstatus(TEST_SUCCESS_TX)

    assert isinstance(result, dict)
    assert 'isError' in result
    assert result['isError'] == '0'  # 0 表示交易成功
    assert 'errDescription' in result


@pytest.mark.asyncio
async def test_getstatus_failed(etherscan):
    """测试获取失败交易的状态"""
    result = await etherscan.transaction.getstatus(TEST_FAILED_TX)

    assert isinstance(result, dict)
    assert 'isError' in result
    assert result['isError'] == '1'  # 1 表示交易失败
    assert 'errDescription' in result
    assert len(result['errDescription']) > 0  # 应该包含错误描述


@pytest.mark.asyncio
async def test_gettxreceiptstatus_success(etherscan):
    """测试获取成功交易的收据状态"""
    result = await etherscan.transaction.gettxreceiptstatus(TEST_SUCCESS_TX)

    assert isinstance(result, dict)
    assert 'status' in result
    # assert result['status'] == '1'  # 1 表示交易成功


@pytest.mark.asyncio
async def test_gettxreceiptstatus_failed(etherscan):
    """测试获取失败交易的收据状态"""
    result = await etherscan.transaction.gettxreceiptstatus(TEST_FAILED_TX)

    assert isinstance(result, dict)
    assert 'status' in result
    # assert result['status'] == '0'  # 0 表示交易失败


# @pytest.mark.asyncio
# async def test_invalid_transaction_hash(etherscan):
#     """测试使用无效的交易哈希"""
#     invalid_hash = "0x0000000000000000000000000000000000000000000000000000000000000000"

#     with pytest.raises(Exception):
#         await etherscan.transaction.getstatus(invalid_hash)

#     with pytest.raises(Exception):
#         await etherscan.transaction.gettxreceiptstatus(invalid_hash)
