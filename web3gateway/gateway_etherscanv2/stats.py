"""
Etherscan Statistics Module

This module provides functionality for network statistics:
- Supply information (ETH, ETH2)
- Price data
- Network metrics
- Chain analysis
"""


class Stats:
    """
    Network statistics API endpoint wrapper.

    Provides methods for retrieving various network statistics
    including supply, price, and chain metrics.

    Attributes:
        client: EtherScanV2 client instance for making API calls
    """

    def __init__(self, client):
        """
        Initialize Stats endpoint wrapper.

        Args:
            client: EtherScanV2 client instance
        """
        self.client = client

    def ethsupply(self):
        """
        Get total ETH supply in circulation.

        Returns:
            str: Total supply in Wei
        """
        return self.client.request("stats", "ethsupply", {})

    def ethsupply2(self, **params):
        """
        Get detailed ETH supply information.

        Returns:
            dict: Supply details containing:
            - EthSupply: Total supply in Wei
            - Eth2Staking: Amount staked in ETH2
            - BurntFees: Total fees burned
            - WithdrawnTotal: Total ETH withdrawn
        """
        return self.client.request("stats", "ethsupply2", params)

    def ethprice(self):
        """
        Get current ETH price and market data.

        Returns:
            dict: Price information containing:
            - ethbtc: ETH/BTC ratio
            - ethbtc_timestamp: BTC price timestamp
            - ethusd: ETH/USD price
            - ethusd_timestamp: USD price timestamp
        """
        return self.client.request("stats", "ethprice", {})

    def chainsize(self, startdate: str, enddate: str,
                  clienttype: str = "geth", syncmode: str = "default",
                  sort: str = "asc"):
        """
        Get blockchain size statistics.

        Args:
            startdate: Start date (YYYY-MM-DD)
            enddate: End date (YYYY-MM-DD)
            clienttype: Client type (default: geth)
            syncmode: Sync mode (default: default)
            sort: Sort direction (asc/desc)

        Returns:
            list: Daily chain size records
        """
        return self.client.request("stats", "chainsize", {
            'startdate': startdate,
            'enddate': enddate,
            'clienttype': clienttype,
            'syncmode': syncmode,
            'sort': sort
        })

    def nodecount(self):
        """
        Get total number of Ethereum nodes.

        Returns:
            dict: Node count information:
            - TotalNodeCount: Number of nodes
            - LastUpdateTimestamp: Last update time
        """
        return self.client.request("stats", "nodecount", {})

    # PRO endpoints with daily statistics
    def dailytxnfee(self, startdate: str, enddate: str, sort: str = "asc"):
        """
        [PRO] Get daily transaction fees.

        Args:
            startdate: Start date (YYYY-MM-DD)
            enddate: End date (YYYY-MM-DD)
            sort: Sort direction (asc/desc)

        Returns:
            list: Daily transaction fee records in Wei
        """
        return self.client.request("stats", "dailytxnfee", {
            'startdate': startdate,
            'enddate': enddate,
            'sort': sort
        })

    def dailynewaddress(self, startdate: str, enddate: str, sort: str = "asc"):
        """ [PRO] Returns the number of new Ethereum addresses created per day.

        Args:
            startdate: Start date in yyyy-MM-dd format
            enddate: End date in yyyy-MM-dd format
            sort: Sort direction ('asc' or 'desc')

        Returns:
            [{
                "UTCDate": "2023-07-01",
                "unixTimeStamp": "1688169600",
                "newAddressCount": "12345"
            }, ...]
        """
        return self.client.request("stats", "dailynewaddress", {
            'startdate': startdate,
            'enddate': enddate,
            'sort': sort
        })

    def dailynetutilization(self, startdate: str, enddate: str, sort: str = "asc"):
        """ [PRO] Returns the daily network utilization percentage.

        Args:
            startdate: Start date in yyyy-MM-dd format
            enddate: End date in yyyy-MM-dd format
            sort: Sort direction ('asc' or 'desc')

        Returns:
            [{
                "UTCDate": "2023-07-01",
                "unixTimeStamp": "1688169600",
                "networkUtilization": "68.45"
            }, ...]
        """
        return self.client.request("stats", "dailynetutilization", {
            'startdate': startdate,
            'enddate': enddate,
            'sort': sort
        })

    def dailyavghashrate(self, **params):
        """ [PRO] Returns the daily average hash rate."""
        return self.client.request("stats", "dailyavghashrate", params)

    def dailytx(self, **params):
        """ [PRO] Returns the daily number of transactions."""
        return self.client.request("stats", "dailytx", params)

    def dailyavgnetdifficulty(self, **params):
        """  [PRO] Returns the daily average network difficulty."""
        return self.client.request("stats", "dailyavgnetdifficulty", params)

    def ethdailymarketcap(self, **params):
        """ [PRO] Returns the daily market cap of Ethereum."""
        return self.client.request("stats", "ethdailymarketcap", params)

    def ethdailyprice(self, **params):
        """
        [PRO] Get historical daily ETH price.

        Args:
            **params: Query parameters including:
                - startdate: Start date (YYYY-MM-DD)
                - enddate: End date (YYYY-MM-DD)
                - sort: Sort direction

        Returns:
            list: Daily price records
        """
        return self.client.request("stats", "ethdailyprice", params)
