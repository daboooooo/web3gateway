# test blockchain gateway

import pytest

from web3gateway.config import load_config_json
from web3gateway.gateway_blockchain import Blockchain


from_address = '0x32f7CB25353F1Acae03ADe9Ca8e91ECAd57Fd7B0'
to_address = '0x32f7CB25353F1Acae03ADe9Ca8e91ECAd57Fd7B0'


@pytest.mark.asyncio
async def test_send_transaction():
    config = load_config_json(None)
    gw = Blockchain(config)
    chain_id = 1
    unsigned_tx = await gw.assemble_unsigned_transaction(chain_id, from_address, to_address, 0, '')
    print(unsigned_tx)
    assert unsigned_tx is not None
    # sign the transaction
    # signed_tx = w3.eth.account.sign_transaction(unsigned_tx, private_key)
    # send the signed transaction
    # tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # wait for the transaction to be mined
    # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
