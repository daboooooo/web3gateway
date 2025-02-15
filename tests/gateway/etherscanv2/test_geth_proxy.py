import pytest

from web3gateway.config import load_config_json
from web3gateway.gateway_etherscanv2 import EtherScanV2


# 测试常量
TEST_BLOCK = "0xED72D8"  # 15537394 (The Merge block)
TEST_TX_HASH = "0x4b61511886d871cd28d2996e7ef1876970207qdbee6f0daa74fc5fc46db58b7c"
TEST_ADDRESS = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"  # Binance hot wallet
TEST_CONTRACT = "0xdac17f958d2ee523a2206206994597c13d831ec7"  # USDT contract


@pytest.fixture
async def etherscan():
    """创建 EtherScanV2 测试实例"""
    config = load_config_json(None)
    instance = await EtherScanV2.create(config)
    instance.set_chain_id(1)  # 使用以太坊主网
    return instance


@pytest.mark.asyncio
async def test_eth_block_number(etherscan):
    """测试获取最新区块号"""
    result = await etherscan.proxy.eth_block_number()
    assert isinstance(result, str)
    assert result.startswith("0x")
    assert int(result, 16) > 0


@pytest.mark.asyncio
async def test_eth_get_block_by_number(etherscan):
    """测试通过区块号获取区块信息"""
    result = await etherscan.proxy.eth_get_block_by_number(TEST_BLOCK, True)
    assert isinstance(result, dict)
    assert result["number"].lower() == TEST_BLOCK.lower()
    assert "hash" in result
    assert "transactions" in result


@pytest.mark.asyncio
async def test_eth_get_transaction_count(etherscan):
    """测试获取账户交易数量"""
    result = await etherscan.proxy.eth_get_transaction_count(TEST_ADDRESS, "latest")
    assert isinstance(result, str)
    assert result.startswith("0x")
    assert int(result, 16) >= 0


@pytest.mark.asyncio
async def test_eth_get_code(etherscan):
    """测试获取合约代码"""
    result = await etherscan.proxy.eth_get_code(TEST_CONTRACT, "latest")
    assert isinstance(result, str)
    assert result.startswith("0x")
    assert len(result) > 2  # 合约代码应该不为空


@pytest.mark.asyncio
async def test_eth_gas_price(etherscan):
    """测试获取当前 gas 价格"""
    result = await etherscan.proxy.eth_gas_price()
    assert isinstance(result, str)
    assert result.startswith("0x")
    assert int(result, 16) > 0


@pytest.mark.asyncio
async def test_eth_get_storage_at(etherscan):
    """测试获取存储数据"""
    result = await etherscan.proxy.eth_get_storage_at(
        TEST_CONTRACT,
        "0x0",
        "latest"
    )
    assert isinstance(result, str)
    assert result.startswith("0x")
