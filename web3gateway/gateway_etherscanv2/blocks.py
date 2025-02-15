"""
Etherscan Blocks Module

This module provides functionality for block-related operations:
- Block rewards
- Block countdown
- Block timing
"""

from typing import Literal


class Blocks:
    """
    Block-related API endpoint wrapper.

    Provides methods for querying block information including
    rewards, countdown times, and block numbers by timestamp.

    Attributes:
        client: EtherScanV2 client instance for making API calls
    """

    def __init__(self, client):
        """
        Initialize Blocks endpoint wrapper.

        Args:
            client: EtherScanV2 client instance
        """
        self.client = client

    async def getblockreward(self, blockno: int):
        """
        Get block reward and fee info.

        Args:
            blockno: Block number to query

        Returns:
            Block reward information
        """
        params = {"blockno": blockno}
        return await self.client.request("block", "getblockreward", params)

    async def getblockcountdown(self, blockno: int):
        """
        Get estimated time remaining until a block.

        Args:
            blockno: Target block number

        Returns:
            Estimated countdown information
        """
        params = {"blockno": blockno}
        return await self.client.request("block", "getblockcountdown", params)

    async def getblocknobytime(self, timestamp: int,
                               closest: Literal["before", "after"] = "before"):
        """
        Get block number by timestamp.

        Args:
            timestamp: Unix timestamp
            closest: Return block before or after timestamp

        Returns:
            Block number information
        """
        params = {"timestamp": timestamp, "closest": closest}
        return await self.client.request("block", "getblocknobytime", params)

    def dailyavgblocksize(self, startdate: str, enddate: str, sort: str = "asc"):
        """ [PRO] Returns the daily average block size within a date range.

        Args:
            startdate: Start date in yyyy-MM-dd format
            enddate: End date in yyyy-MM-dd format
            sort: 'asc' or 'desc'

        Returns:
            [
                {
                    "UTCDate": "2023-07-01",
                    "unixTimeStamp": "1688169600",
                    "blockSize_bytes": "120764"
                },
                ...
            ]
        """
        return self.client.request(
            "stats", "dailyavgblocksize",
            {'startdate': startdate, 'enddate': enddate, 'sort': sort})

    def dailyblkcount(self, startdate: str, enddate: str, sort: str = "asc"):
        """ [PRO] Returns the number of blocks mined daily within a date range.

        Args:
            startdate: Start date in yyyy-MM-dd format
            enddate: End date in yyyy-MM-dd format
            sort: 'asc' or 'desc'

        Returns:
            [
                {
                    "UTCDate": "2023-07-01",
                    "unixTimeStamp": "1688169600",
                    "blockCount": "7123"
                },
                ...
            ]
        """
        return self.client.request(
            "stats", "dailyblkcount",
            {'startdate': startdate, 'enddate': enddate, 'sort': sort})

    def dailyblockrewards(self, startdate: str, enddate: str, sort: str = "asc"):
        """ [PRO] Returns the daily block rewards within a date range.

        Args:
            startdate: Start date in yyyy-MM-dd format
            enddate: End date in yyyy-MM-dd format
            sort: 'asc' or 'desc'

        Returns:
            [
                {
                    "UTCDate": "2023-07-01",
                    "unixTimeStamp": "1688169600",
                    "blockRewards_Eth": "1234.56"
                },
                ...
            ]
        """
        return self.client.request(
            "stats", "dailyblockrewards",
            {'startdate': startdate, 'enddate': enddate, 'sort': sort})

    def dailyavgblocktime(self, startdate: str, enddate: str, sort: str = "asc"):
        """ [PRO] Returns the daily average block time within a date range.

        Args:
            startdate: Start date in yyyy-MM-dd format
            enddate: End date in yyyy-MM-dd format
            sort: 'asc' or 'desc'

        Returns:
            [
                {
                    "UTCDate": "2023-07-01",
                    "unixTimeStamp": "1688169600",
                    "blockTime_sec": "12.12"
                },
                ...
            ]
        """
        return self.client.request(
            "stats", "dailyavgblocktime",
            {'startdate': startdate, 'enddate': enddate, 'sort': sort})

    def dailyuncleblkcount(self, startdate: str, enddate: str, sort: str = "asc"):
        """ [PRO] Returns the number of 'Uncle' blocks mined daily within a date range.

        Args:
            startdate: Start date in yyyy-MM-dd format
            enddate: End date in yyyy-MM-dd format
            sort: 'asc' or 'desc'

        Returns:
            [
                {
                    "UTCDate": "2023-07-01",
                    "unixTimeStamp": "1688169600",
                    "uncleBlockCount": "123"
                },
                ...
            ]
        """
        return self.client.request(
            "stats", "dailyuncleblkcount",
            {'startdate': startdate, 'enddate': enddate, 'sort': sort})
