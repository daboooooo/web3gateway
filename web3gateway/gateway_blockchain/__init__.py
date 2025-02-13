from functools import reduce
from typing import Any

from web3 import AsyncHTTPProvider, AsyncWeb3

from web3gateway.utils.chains_json import Chains


MODE = {
    "slow": [10.0, 20.0, 30.0, 40.0, 50.0],  # <1min
    "normal": [10.0, 30.0, 50.0, 70.0, 90.0],  # <30sec
    "fast": [50.0, 60.0, 70.0, 80.0, 90.0],  # <10sec
}


class Blockchain:
    """ Blockchain gateway """

    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.web3_instances: dict[int, AsyncWeb3] = {}
        self.chains = Chains(infura_project_id=self.config["infura_project_id"])
        if not self.chains.load_chains_json_file():
            self.chains.update_chains_json()

    def _get_web3_instance(self, chain_id: int) -> AsyncWeb3:
        if chain_id not in self.web3_instances:
            # initialize web3 instance
            if not self.chains.select_chain_by_key_value("chainId", chain_id):
                raise ValueError(f"Chain {chain_id} not supported")
            rpc_urls = self.chains.get_selected_chain_value("rpc")
            if not rpc_urls:
                raise ValueError(f"No rpc url found for Chain {chain_id}")
            rpc_url = rpc_urls[0]
            self.web3_instances[chain_id] = AsyncWeb3(AsyncHTTPProvider(rpc_url))
        return self.web3_instances[chain_id]

    async def get_nonce(self, chain_id: int, address):
        """ get nonce for the address """
        web3 = self._get_web3_instance(chain_id)
        return await web3.eth.get_transaction_count(address)

    async def estimate_gas(self, chain_id: int, tx_params):
        """ estimate gas that will be used by the transaction """
        web3 = self._get_web3_instance(chain_id)
        return await web3.eth.estimate_gas(tx_params)

    async def get_gas_price(self, chain_id: int, gas_level):
        """ get gas price for the transaction """
        web3 = self._get_web3_instance(chain_id)
        if gas_level not in MODE:
            raise ValueError(f"Gas level {gas_level} not supported, should be one of {MODE.keys()}")
        try:
            # baseFee:
            # Set by blockchain, varies at each block, always burned
            block_info = await web3.eth.get_block('pending')
            base_fee = block_info.get('baseFeePerGas')

            # next baseFee:
            # Overestimation of baseFee in next block
            # difference always refunded
            next_base_fee = base_fee * 2 if base_fee is not None else 100000

            # priorityFee:
            # Set by user, tip/reward paid directly to miners, never returned
            fee_history = await web3.eth.fee_history(3, 'pending', MODE[gas_level])
            reward_history = fee_history.get('reward')
            rewards = reduce(lambda x, y: x + y, reward_history)
            avg_reward = sum(rewards) // len(rewards)

            # Estimations:
            # maxFee - (maxPriorityFee + baseFee actually paid) = \
            # Returned to used
            return {"maxPriorityFeePerGas": avg_reward,
                    "maxFeePerGas": avg_reward + next_base_fee}
        except Exception:
            gas_price = await web3.eth.gas_price
            return {"gasPrice": gas_price}

    async def assemble_unsigned_transaction(self, chain_id: int,
                                            from_address: str, to_address: str,
                                            value: int, data: str,
                                            gas_level: str = "normal") -> dict[str, Any]:
        """ assemble an unsigned transaction """
        nonce = await self.get_nonce(chain_id, from_address)
        transaction = {
            'from': from_address,
            'to': to_address,
            'value': value,
            'nonce': nonce,
            'chainId': chain_id,
        }
        if data:
            transaction['data'] = data
        # estimate gas
        gas = await self.estimate_gas(chain_id, transaction)
        transaction['gas'] = gas
        # gas price
        gas_price = await self.get_gas_price(chain_id, gas_level)
        transaction.update(gas_price)
        return transaction

    async def send_raw_transaction(self, chain_id: int, raw_tx) -> str:
        """ send a raw transaction """
        web3 = self._get_web3_instance(chain_id)
        tx_hash = await web3.eth.send_raw_transaction(raw_tx)
        return tx_hash.hex()

    async def get_transaction_receipt(self, chain_id: int, tx_hash):
        """ get transaction receipt """
        web3 = self._get_web3_instance(chain_id)
        return await web3.eth.get_transaction_receipt(tx_hash)

    async def wait_for_transaction_receipt(self, chain_id: int, tx_hash):
        """ wait for transaction receipt """
        web3 = self._get_web3_instance(chain_id)
        return await web3.eth.wait_for_transaction_receipt(tx_hash)
