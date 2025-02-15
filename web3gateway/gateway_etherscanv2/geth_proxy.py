from . import EtherScanV2


class Proxy:
    """Geth/Parity Proxy APIs from Etherscan
    https://docs.etherscan.io/etherscan-v2/api-endpoints/geth-parity-proxy
    """

    def __init__(self, etherscan: EtherScanV2):
        self.etherscan = etherscan

    def eth_block_number(self):
        """Returns the latest block number.
        Returns:
            Hex string of the current block number the client is on.
        """
        return self.etherscan.request("proxy", "eth_blockNumber", {})

    def eth_get_block_by_number(self, tag: str, boolean: bool):
        """Returns information about a block by block number.
        Args:
            tag: Tag or block number in hex
            boolean: True for full transaction objects, false for hashes
        """
        return self.etherscan.request("proxy", "eth_getBlockByNumber",
                                      {'tag': tag, 'boolean': str(boolean).lower()})

    def eth_get_uncle_by_block_number_and_index(self, tag: str, index: str):
        """Returns information about an uncle by block number and uncle index position.
        Args:
            tag: Tag or block number in hex
            index: Uncle index position in hex
        """
        return self.etherscan.request("proxy", "eth_getUncleByBlockNumberAndIndex",
                                      {'tag': tag, 'index': index})

    def eth_get_block_transaction_count_by_number(self, tag: str):
        """Returns the number of transactions in a block.
        Args:
            tag: Tag or block number in hex
        Returns:
            Number of transactions in the block in hex
        """
        return self.etherscan.request("proxy", "eth_getBlockTransactionCountByNumber",
                                      {'tag': tag})

    def eth_get_transaction_by_hash(self, txhash: str):
        """Returns the information about a transaction requested by transaction hash.
        Args:
            txhash: Transaction hash
        """
        return self.etherscan.request("proxy", "eth_getTransactionByHash",
                                      {'txhash': txhash})

    def eth_get_transaction_by_block_number_and_index(self, tag: str, index: str):
        """Returns information about a transaction by block number and transaction index position.
        Args:
            tag: Tag or block number in hex
            index: Transaction index position in hex
        """
        return self.etherscan.request("proxy", "eth_getTransactionByBlockNumberAndIndex",
                                      {'tag': tag, 'index': index})

    def eth_get_transaction_count(self, address: str, tag: str = "latest"):
        """Returns the number of transactions sent from an address.
        Args:
            address: Address to get transaction count for
            tag: Tag or block number in hex, or "latest", "earliest" or "pending"
        """
        return self.etherscan.request("proxy", "eth_getTransactionCount",
                                      {'address': address, 'tag': tag})

    def eth_send_raw_transaction(self, hex_: str):
        """Submits a pre-signed transaction for broadcast to the Ethereum network.
        Args:
            hex: The signed transaction data
        """
        return self.etherscan.request("proxy", "eth_sendRawTransaction", {'hex': hex_})

    def eth_get_transaction_receipt(self, txhash: str):
        """Returns the receipt of a transaction by transaction hash.
        Args:
            txhash: Transaction hash
        """
        return self.etherscan.request("proxy", "eth_getTransactionReceipt",
                                      {'txhash': txhash})

    def eth_call(self, to: str, data: str, tag: str = "latest"):
        """Executes a new message call immediately without creating a transaction.
        Args:
            to: Contract address
            data: Hash of the method signature and encoded parameters
            tag: Tag or block number in hex, or "latest", "earliest" or "pending"
        """
        return self.etherscan.request("proxy", "eth_call",
                                      {'to': to, 'data': data, 'tag': tag})

    def eth_get_code(self, address: str, tag: str = "latest"):
        """Returns code at a given address.
        Args:
            address: Address to get code from
            tag: Tag or block number in hex, or "latest", "earliest" or "pending"
        """
        return self.etherscan.request("proxy", "eth_getCode",
                                      {'address': address, 'tag': tag})

    def eth_get_storage_at(self, address: str, position: str, tag: str = "latest"):
        """Returns the value from a storage position at a given address.
        Args:
            address: Address of the storage
            position: Position in the storage
            tag: Tag or block number in hex, or "latest", "earliest" or "pending"
        """
        return self.etherscan.request("proxy", "eth_getStorageAt",
                                      {'address': address, 'position': position, 'tag': tag})

    def eth_gas_price(self):
        """Returns the current price per gas in wei.
        Returns:
            Current gas price in wei as hex string
        """
        return self.etherscan.request("proxy", "eth_gasPrice", {})

    def eth_estimate_gas(self, data: str, to: str, value: str,
                         gas: str, gasprice: str):
        """Makes a call or transaction and returns the used gas.
        Args:
            data: The hash of the method signature and encoded parameters
            to: Contract address
            value: Value sent in wei
            gas: Gas provided for the transaction
            gasprice: Gas price provided for the transaction
        """
        return self.etherscan.request("proxy", "eth_estimateGas",
                                      {'data': data, 'to': to, 'value': value,
                                       'gas': gas, 'gasprice': gasprice})
