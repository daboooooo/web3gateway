"""
Etherscan Gas Tracker Module

This module provides functionality for gas-related operations:
- Gas price estimation
- Gas oracle information
- Historical gas statistics
"""


class GasTracker:
    """
    Gas tracking API endpoint wrapper.

    Provides methods for monitoring and estimating gas prices,
    including historical data and real-time oracle information.

    Attributes:
        client: EtherScanV2 client instance for making API calls
    """

    def __init__(self, client):
        """
        Initialize GasTracker endpoint wrapper.

        Args:
            client: EtherScanV2 client instance
        """
        self.client = client

    def gasestimate(self, gasprice: int):
        """
        Estimate gas usage for a given gas price.

        Args:
            gasprice: Gas price in Wei

        Returns:
            Estimated gas consumption in units
        """
        return self.client.request("gastracker", "gasestimate", {'gasprice': gasprice})

    def gasoracle(self):
        """
        Get current gas oracle data.

        Returns:
            Dict containing:
            - SafeLow: Safe low gas price
            - Standard: Standard gas price
            - Fast: Fast gas price
            - Fastest: Fastest gas price
            - ProposeGasPrice: Suggested gas price
        """
        return self.client.request("gastracker", "gasoracle", {})

    def dailyavggaslimit(self, startdate: str, enddate: str, sort: str = 'asc'):
        """
        Get historical daily average gas limit data.

        Args:
            startdate: Start date in YYYY-MM-DD format (e.g., 2019-02-01)
            enddate: End date in YYYY-MM-DD format
            sort: Sort order ('asc' or 'desc')

        Returns:
            List of daily gas limit records containing:
            - UTCDate: Date in YYYY-MM-DD format
            - unixTimeStamp: Unix timestamp
            - gasLimit: Average gas limit for the day
        """
        return self.client.request(
            "stats", "dailyavggaslimit",
            {
                'startdate': startdate,
                'enddate': enddate,
                'sort': sort
            })

    def dailygasused(self, **params):
        """
        Get daily gas consumption statistics [PRO].

        Args:
            **params: Query parameters including:
                - startdate: Start date (YYYY-MM-DD)
                - enddate: End date (YYYY-MM-DD)
                - sort: Sort order

        Returns:
            Daily gas usage statistics
        """
        return self.client.request("stats", "dailygasused", params)

    def dailyavggasprice(self, **params):
        """
        Get daily average gas price statistics [PRO].

        Args:
            **params: Query parameters including:
                - startdate: Start date (YYYY-MM-DD)
                - enddate: End date (YYYY-MM-DD)
                - sort: Sort order

        Returns:
            Daily average gas price statistics
        """
        return self.client.request("stats", "dailyavggasprice", params)
