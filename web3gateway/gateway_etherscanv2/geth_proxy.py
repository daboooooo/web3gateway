"""
Ethereum JSON-RPC Proxy Module

This module provides Ethereum JSON-RPC compatibility layer through Etherscan:
- Standard Ethereum JSON-RPC methods
- Block queries and manipulation
- Transaction operations
- Smart contract interactions
"""


class Proxy:
    """
    Ethereum JSON-RPC compatible API endpoint wrapper.

    Implements standard Ethereum JSON-RPC methods through Etherscan's proxy,
    allowing seamless integration with existing Ethereum tools and libraries.

    Attributes:
        client: EtherScanV2 client instance for making API calls
    """

    def __init__(self, client):
        """
        Initialize Proxy endpoint wrapper.

        Args:
            client: EtherScanV2 client instance
        """
        self.client = client

    def eth_block_number(self):
        """
        Get the latest block number.

        Returns:
            str: Hex string of current block number (e.g., '0x4b7')
        """
        return self.client.request("proxy", "eth_blockNumber", {})

    def eth_get_block_by_number(self, tag: str, boolean: bool):
        """
        Get information about a block by its number.

        Args:
            tag: Block number in hex or tag (latest/pending/earliest)
            boolean: True for full transactions, false for tx hashes

        Returns:
            dict: Block information including transactions
        """
        return self.client.request(
            "proxy", "eth_getBlockByNumber",
            {'tag': tag, 'boolean': str(boolean).lower()})

    def eth_get_uncle_by_block_number_and_index(self, tag: str, index: str):
        """Returns information about an uncle by block number and uncle index position.
        Args:
            tag: Tag or block number in hex
            index: Uncle index position in hex
        """
        return self.client.request(
            "proxy", "eth_getUncleByBlockNumberAndIndex",
            {'tag': tag, 'index': index})

    def eth_get_block_transaction_count_by_number(self, tag: str):
        """Returns the number of transactions in a block.
        Args:
            tag: Tag or block number in hex
        Returns:
            Number of transactions in the block in hex
        """
        return self.client.request(
            "proxy", "eth_getBlockTransactionCountByNumber",
            {'tag': tag})

    def eth_get_transaction_by_hash(self, txhash: str):
        """Returns the information about a transaction requested by transaction hash.
        Args:
            txhash: Transaction hash
        """
        return self.client.request(
            "proxy", "eth_getTransactionByHash",
            {'txhash': txhash})

    def eth_get_transaction_by_block_number_and_index(self, tag: str, index: str):
        """Returns information about a transaction by block number and transaction index position.
        Args:
            tag: Tag or block number in hex
            index: Transaction index position in hex
        """
        return self.client.request(
            "proxy", "eth_getTransactionByBlockNumberAndIndex",
            {'tag': tag, 'index': index})

    def eth_get_transaction_count(self, address: str, tag: str = "latest"):
        """
        Get the number of transactions sent from an address.

        Args:
            address: Account address to query
            tag: Block number or tag (latest/pending/earliest)

        Returns:
            str: Number of transactions in hex format
        """
        return self.client.request(
            "proxy", "eth_getTransactionCount",
            {'address': address, 'tag': tag})

    def eth_send_raw_transaction(self, hex_: str):
        """
        Broadcast a signed transaction.

        Args:
            hex_: Signed transaction data in hex format

        Returns:
            str: Transaction hash if successful

        Note:
            Transaction must be signed before sending
        """
        return self.client.request("proxy", "eth_sendRawTransaction", {'hex': hex_})

    def eth_get_transaction_receipt(self, txhash: str):
        """Returns the receipt of a transaction by transaction hash.
        Args:
            txhash: Transaction hash
        """
        return self.client.request(
            "proxy", "eth_getTransactionReceipt",
            {'txhash': txhash})

    def eth_call(self, to: str, data: str, tag: str = "latest"):
        """
        Execute a new message call without creating a transaction.

        Args:
            to: Target contract address
            data: Encoded call data (method signature + parameters)
            tag: Block number or tag (latest/pending/earliest)

        Returns:
            str: Result of the contract call in hex format
        """
        return self.client.request(
            "proxy", "eth_call", {'to': to, 'data': data, 'tag': tag})

    def eth_get_code(self, address: str, tag: str = "latest"):
        """
        Get the deployed bytecode at an address.

        Args:
            address: Contract address
            tag: Block number or tag (latest/pending/earliest)

        Returns:
            str: Contract bytecode in hex format
        """
        return self.client.request(
            "proxy", "eth_getCode", {'address': address, 'tag': tag})

    def eth_get_storage_at(self, address: str, position: str, tag: str = "latest"):
        """Returns the value from a storage position at a given address.
        Args:
            address: Address of the storage
            position: Position in the storage
            tag: Tag or block number in hex, or "latest", "earliest" or "pending"
        """
        return self.client.request(
            "proxy", "eth_getStorageAt",
            {'address': address, 'position': position, 'tag': tag})

    def eth_gas_price(self):
        """
        Get the current gas price.

        Returns:
            str: Current gas price in wei (hex format)
        """
        return self.client.request("proxy", "eth_gasPrice", {})

    def eth_estimate_gas(self, data: str, to: str, value: str,
                         gas: str, gasprice: str):
        """
        Estimate gas needed for a transaction.

        Args:
            data: Transaction data (method call + parameters)
            to: Target contract address
            value: Amount of ETH to send in wei
            gas: Gas limit
            gasprice: Gas price in wei

        Returns:
            str: Estimated gas amount in hex format
        """
        return self.client.request(
            "proxy", "eth_estimateGas",
            {'data': data, 'to': to, 'value': value, 'gas': gas, 'gasprice': gasprice})
