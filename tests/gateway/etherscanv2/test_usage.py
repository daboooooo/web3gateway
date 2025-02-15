import pytest

from web3gateway.config import load_config_json
from web3gateway.gateway_etherscanv2 import EtherScanV2


@pytest.fixture
async def etherscan():
    """创建 EtherScanV2 测试实例"""
    config = load_config_json(None)
    instance = await EtherScanV2.create(config)
    instance.set_chain_id(1)  # 使用以太坊主网
    return instance


@pytest.mark.asyncio
async def test_getapilimit(etherscan):
    """测试获取API限制信息"""
    result = await etherscan.usage.getapilimit()

    assert isinstance(result, dict)
    # 检查所有必需的字段
    assert 'creditsUsed' in result
    assert 'creditsAvailable' in result
    assert 'creditLimit' in result
    assert 'limitInterval' in result
    assert isinstance(result['creditsUsed'], int)
    assert isinstance(result['creditsAvailable'], int)
    assert isinstance(result['creditLimit'], int)
    # 验证数值的合理性
    assert result['creditsUsed'] >= 0
    assert result['creditsAvailable'] >= 0
    assert result['creditLimit'] > 0
    assert result['creditsUsed'] + result['creditsAvailable'] == result['creditLimit']


@pytest.mark.asyncio
async def test_chainlist(etherscan):
    """测试获取支持的区块链列表"""
    result = etherscan.usage.chainlist()

    assert isinstance(result, list)
    assert len(result) > 0

    # 测试第一个链（应该是以太坊主网）
    eth_mainnet = result[0]
    assert isinstance(eth_mainnet, dict)
    assert eth_mainnet['chainid'] == '1'
    assert eth_mainnet['chainname'] == 'Ethereum Mainnet'
    assert 'etherscan.io' in eth_mainnet['blockexplorer']
    assert 'api.etherscan.io' in eth_mainnet['apiurl']
    assert eth_mainnet['status'] == 1

    # 检查所有链的必需字段
    for chain in result:
        assert 'chainname' in chain
        assert 'chainid' in chain
        assert 'blockexplorer' in chain
        assert 'apiurl' in chain
        assert 'status' in chain
