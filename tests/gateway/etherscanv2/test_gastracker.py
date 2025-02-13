import pytest

from web3gateway.config import load_config_json
from web3gateway.gateway_etherscanv2 import EtherScanV2


@pytest.mark.asyncio
async def test_gasoracle():
    """ test gasoracle """
    config = load_config_json(None)
    instance = EtherScanV2(config)
    instance.set_chain_id(1)
    assert instance.chain_id == 1
    result = await instance.gas_tracker.gasoracle()
    print(result)
    assert result is not None
