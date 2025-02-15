from . import EtherScanV2


class Logs:
    """Log APIs from Etherscan
    https://docs.etherscan.io/etherscan-v2/api-endpoints/logs
    """

    def __init__(self, etherscan: 'EtherScanV2'):
        self.etherscan = etherscan

    def get_logs_by_address(self, address: str,
                            from_block: int, to_block: int,
                            page: int, offset: int):
        """Returns the events log for a specific address.

        Args:
            address: Contract address
            fromBlock: Start block number
            toBlock: End block number
            page: Page number
            offset: Max records to return
            topic0: Topics to filter by

        Returns:
            {
                "address": "0x...",
                "topics": [...],
                "data": "0x...",
                "blockNumber": "0x...",
                "timeStamp": "0x...",
                "gasPrice": "0x...",
                "gasUsed": "0x...",
                "logIndex": "0x...",
                "transactionHash": "0x...",
                "transactionIndex": "0x..."
            }
        """
        params = {
            'address': address,
            'fromBlock': from_block,
            'toBlock': to_block,
            'page': page,
            'offset': offset}
        return self.etherscan.request("logs", "getLogs", params)

    def get_logs_by_topic(
            self, address: str,
            from_block: int, to_block: int,
            topic0: str, topic0_1_opr: str, topic1: str,
            page: int, offset: int):
        """Returns the events log for a specific topic.

        Args:
            address: Contract address
            fromBlock: Start block number
            toBlock: End block number
            page: Page number
            offset: Max records to return
            topic0: Topics to filter by

        Returns:
            {
                "address": "0x...",
                "topics": [...],
                "data": "0x...",
                "blockNumber": "0x...",
                "timeStamp": "0x...",
                "gasPrice": "0x...",
                "gasUsed": "0x...",
                "logIndex": "0x...",
                "transactionHash": "0x...",
                "transactionIndex": "0x..."
            }
        """
        params = {
            'address': address,
            'fromBlock': from_block,
            'toBlock': to_block,
            'topic0': topic0,
            'topic0_1_opr': topic0_1_opr,
            'topic1': topic1,
            'page': page,
            'offset': offset
        }
        return self.etherscan.request("logs", "getLogs", params)

    def get_logs_by_address_filted_by_topic(
            self, from_block: int, to_block: int,
            address: str, topic0: str, topic0_1_opr: str, topic1: str,
            page: int, offset: int):
        """Returns the events log for a specific address and topic.

        Args:
            address: Contract address
            fromBlock: Start block number
            toBlock: End block number
            page: Page number
            offset: Max records to return
            topic0: Topics to filter by

        Returns:
            {
                "address": "0x...",
                "topics": [...],
                "data": "0x...",
                "blockNumber": "0x...",
                "timeStamp": "0x...",
                "gasPrice": "0x...",
                "gasUsed": "0x...",
                "logIndex": "0x...",
                "transactionHash": "0x...",
                "transactionIndex": "0x..."
            }
        """
        params = {
            'fromBlock': from_block,
            'toBlock': to_block,
            'address': address,
            'topic0': topic0,
            'topic0_1_opr': topic0_1_opr,
            'topic1': topic1,
            'page': page,
            'offset': offset
        }
        return self.etherscan.request("logs", "getLogs", params)
