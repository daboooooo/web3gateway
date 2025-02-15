"""
Etherscan Event Logs Module

This module provides functionality for querying blockchain event logs:
- Event logs by address
- Event logs by topic
- Filtered event logs with topic combinations
"""


class Logs:
    """
    Event logs API endpoint wrapper.

    Provides methods for retrieving and filtering blockchain event logs
    with support for address and topic-based queries.

    Attributes:
        client: EtherScanV2 client instance for making API calls
    """

    def __init__(self, client):
        """
        Initialize Logs endpoint wrapper.

        Args:
            client: EtherScanV2 client instance
        """
        self.client = client

    def get_logs_by_address(self, address: str,
                            from_block: int, to_block: int,
                            page: int, offset: int):
        """
        Get event logs for a specific address.

        Args:
            address: Contract address to query
            from_block: Starting block number
            to_block: Ending block number
            page: Page number for pagination
            offset: Number of records per page

        Returns:
            List of event logs containing:
            - address: Contract address
            - topics: List of event topics
            - data: Event data in hex
            - blockNumber: Block number in hex
            - timeStamp: Block timestamp in hex
            - gasPrice: Gas price in hex
            - gasUsed: Gas used in hex
            - logIndex: Log index in block
            - transactionHash: Transaction hash
            - transactionIndex: Transaction index in block
        """
        params = {
            'address': address,
            'fromBlock': from_block,
            'toBlock': to_block,
            'page': page,
            'offset': offset
        }
        return self.client.request("logs", "getLogs", params)

    def get_logs_by_topic(
            self, address: str,
            from_block: int, to_block: int,
            topic0: str, topic0_1_opr: str, topic1: str,
            page: int, offset: int):
        """
        Get event logs filtered by topic.

        Args:
            address: Contract address
            from_block: Starting block number
            to_block: Ending block number
            topic0: First topic to filter by (usually event signature)
            topic0_1_opr: Operator between topic0 and topic1 (and/or)
            topic1: Second topic to filter by
            page: Page number for pagination
            offset: Number of records per page

        Returns:
            List of filtered event logs with same structure as get_logs_by_address

        Note:
            Topics are used to filter events based on their indexed parameters
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
        return self.client.request("logs", "getLogs", params)

    def get_logs_by_address_filted_by_topic(
            self, from_block: int, to_block: int,
            address: str, topic0: str, topic0_1_opr: str, topic1: str,
            page: int, offset: int):
        """
        Get event logs for an address filtered by multiple topics.

        Args:
            from_block: Starting block number
            to_block: Ending block number
            address: Contract address
            topic0: First topic filter
            topic0_1_opr: Logic operator between topics (and/or)
            topic1: Second topic filter
            page: Page number for pagination
            offset: Number of records per page

        Returns:
            List of filtered event logs with same structure as get_logs_by_address

        Note:
            This method combines address and topic filtering for more precise queries
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
        return self.client.request("logs", "getLogs", params)
