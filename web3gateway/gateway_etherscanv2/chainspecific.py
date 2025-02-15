"""
Chain-Specific Operations Module

This module provides functionality for chain-specific operations:
- Bridge transactions
- Chain-specific queries
- Network-specific features
"""


class ChainSpecific:
    """
    Chain-specific API endpoint wrapper.

    Provides methods for accessing network-specific features and data
    that are unique to certain blockchain networks.

    Attributes:
        client: EtherScanV2 client instance for making API calls
    """

    def __init__(self, client):
        """
        Initialize ChainSpecific endpoint wrapper.

        Args:
            client: EtherScanV2 client instance
        """
        self.client = client

    def txnbridge(self, address: str):
        """
        Get bridge transactions for an address.

        Args:
            address: Account address to query

        Returns:
            List of bridge transactions
        """
        return self.client.request("account", "txnbridge", {
            "address": address
        })
