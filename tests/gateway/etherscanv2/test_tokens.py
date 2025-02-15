import pytest

from web3gateway.config import load_config_json
from web3gateway.gateway_etherscanv2 import EtherScanV2


# 测试用的合约地址和账户地址
TEST_CONTRACTS = {
    'USDT': '0xdac17f958d2ee523a2206206994597c13d831ec7',
    'USDC': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
    'WETH': '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
}
TEST_ADDRESS = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"  # Binance热钱包


@pytest.fixture
async def etherscan():
    """创建 EtherScanV2 测试实例"""
    config = load_config_json(None)
    instance = await EtherScanV2.create(config)
    instance.set_chain_id(1)  # 使用以太坊主网
    return instance


@pytest.mark.asyncio
@pytest.mark.parametrize("token_name,contract_address", TEST_CONTRACTS.items())
async def test_tokensupply(etherscan, token_name, contract_address):
    """测试获取各种代币的总供应量"""
    result = await etherscan.tokens.tokensupply(contract_address)

    assert result is not None
    assert isinstance(result, str)
    assert int(result) > 0
    print(f"{token_name} total supply: {result}")


@pytest.mark.asyncio
@pytest.mark.parametrize("token_name,contract_address", TEST_CONTRACTS.items())
async def test_tokenbalance(etherscan, token_name, contract_address):
    """测试获取Binance热钱包中各种代币的余额"""
    result = await etherscan.tokens.tokenbalance(
        contractaddress=contract_address,
        address=TEST_ADDRESS,
        tag="latest"
    )

    assert result is not None
    assert isinstance(result, str)
    # 余额可能为0，所以只判断是否为整数
    assert int(result) >= 0
    print(f"Binance hot wallet {token_name} balance: {result}")


# 以下为PRO API功能，暂不测试
# tokenbalance
# tokensupplyhistory
# tokenbalancehistory
# tokenholderlist
# tokeninfo
# addresstokenbalance
# addresstokennftbalance
# addresstokennftinventory
