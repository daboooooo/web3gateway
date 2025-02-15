from . import EtherScanV2


class Blocks:
    """Block APIs from Etherscan
    https://docs.etherscan.io/etherscan-v2/api-endpoints/blocks
    """

    def __init__(self, etherscan: 'EtherScanV2'):
        self.etherscan = etherscan

    def getblockreward(self, blockno: int):
        """Returns the block reward and 'Uncle' block rewards for a given block number.

        Args:
            blockno: Block number

        Returns:
            {
                "blockNumber": "2165403",
                "timeStamp": "1472533979",
                "blockMiner": "0x13a06d3dfe21e0db5c016c03ea7d2509f7f8d1e3",
                "blockReward": "5314181600000000000",
                "uncles": [
                    {
                        "miner": "0xbcdfc35b86bedf72f0cda046a3c16829a2ef41d1",
                        "unclePosition": "0",
                        "blockreward": "3750000000000000000"
                    }
                ],
                "uncleInclusionReward": "312500000000000000"
            }
        """
        return self.etherscan.request("block", "getblockreward", {'blockno': blockno})

    def getblockcountdown(self, blockno: int):
        """Returns the estimated time remaining, in seconds, until a certain block is mined.

        Args:
            blockno: Target future block number

        Returns:
            {
                "CurrentBlock": "16692436",
                "CountdownBlock": "16692499",
                "RemainingBlock": "63",
                "EstimateTimeInSec": "755.0"
            }
        """
        return self.etherscan.request("block", "getblockcountdown", {'blockno': blockno})

    def getblocknobytime(self, timestamp: int, closest: str = "before"):
        """Returns the block number that was mined at a given timestamp.

        Args:
            timestamp: Unix timestamp in seconds
            closest: 'before' or 'after' - Search for block before or after timestamp

        Returns:
            Block number as string, e.g. "16691395"
        """
        return self.etherscan.request("block", "getblocknobytime",
                                      {'timestamp': timestamp, 'closest': closest})

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
        return self.etherscan.request("stats", "dailyavgblocksize",
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
        return self.etherscan.request("stats", "dailyblkcount",
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
        return self.etherscan.request("stats", "dailyblockrewards",
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
        return self.etherscan.request("stats", "dailyavgblocktime",
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
        return self.etherscan.request("stats", "dailyuncleblkcount",
                                      {'startdate': startdate, 'enddate': enddate, 'sort': sort})
