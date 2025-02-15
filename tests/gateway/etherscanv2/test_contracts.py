import pytest

from web3gateway.config import load_config_json
from web3gateway.gateway_etherscanv2 import EtherScanV2


# 测试用的合约地址
TEST_CONTRACT = "0xdAC17F958D2ee523a2206206994597C13D831ec7"  # USDT contract
TEST_CONTRACTS = [
    "0xdAC17F958D2ee523a2206206994597C13D831ec7",  # USDT
    "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"   # WETH
]


@pytest.fixture
async def etherscan():
    """创建 EtherScanV2 测试实例"""
    config = load_config_json(None)
    instance = await EtherScanV2.create(config)
    instance.set_chain_id(1)  # 使用以太坊主网
    return instance


@pytest.mark.asyncio
async def test_getabi(etherscan):
    """测试获取合约 ABI"""
    result = await etherscan.contract.getabi(TEST_CONTRACT)
    assert isinstance(result, str)
    assert result.startswith('[')  # ABI 应该是 JSON 数组格式
    assert result.endswith(']')


@pytest.mark.asyncio
async def test_getsourcecode(etherscan):
    """测试获取合约源代码"""
    result = await etherscan.contract.getsourcecode(TEST_CONTRACT)
    assert isinstance(result, list)
    assert len(result) > 0
    contract_info = result[0]
    assert 'SourceCode' in contract_info
    assert 'ContractName' in contract_info
    assert 'CompilerVersion' in contract_info


@pytest.mark.asyncio
async def test_getcontractcreation(etherscan):
    """测试获取合约创建信息"""
    contract_addresses = ",".join(TEST_CONTRACTS)
    result = await etherscan.contract.getcontractcreation(contract_addresses)
    assert isinstance(result, list)
    assert len(result) == len(TEST_CONTRACTS)
    for contract_info in result:
        assert 'contractAddress' in contract_info
        assert 'contractCreator' in contract_info
        assert 'txHash' in contract_info


# 注意：以下测试用例需要实际的合约代码和参数才能运行
# 这些API通常用于合约验证过程


@pytest.mark.skip(reason="需要实际的合约代码和参数")
@pytest.mark.asyncio
async def test_verify_contract_flow(etherscan):
    """测试合约验证流程"""
    # 1. 验证合约源码
    verification_params = {
        "sourceCode": "contract test { }",
        "contractname": "Test",
        "compilerversion": "v0.8.0",
        "optimizationUsed": "0",
        "address": "0x..."
    }
    guid = await etherscan.contract.verifysourcecode(**verification_params)
    assert isinstance(guid, str)

    # 2. 检查验证状态
    status = await etherscan.contract.checkverifystatus(guid)
    assert isinstance(status, str)
