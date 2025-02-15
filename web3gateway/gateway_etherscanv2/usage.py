"""
Etherscan API Usage Module

This module provides functionality for monitoring API usage:
- API rate limits and quotas
- API credit tracking
- Chain support information
"""

import requests


class Usage:
    """
    API usage monitoring endpoint wrapper.

    Provides methods for checking API limits and available chains,
    helping manage API quotas and service availability.

    Attributes:
        client: EtherScanV2 client instance for making API calls
    """

    def __init__(self, client):
        """
        Initialize Usage endpoint wrapper.

        Args:
            client: EtherScanV2 client instance
        """
        self.client = client

    def getapilimit(self):
        """
        Get current API usage and limit information.

        Returns:
            dict: API limit details containing:
            - creditsUsed: Number of API calls used
            - creditsAvailable: Remaining API calls
            - creditLimit: Total API call limit
            - limitInterval: Reset interval (e.g., "daily")
            - intervalExpiryTimespan: Time until limit reset
        """
        return self.client.request("getapilimit", "getapilimit", {})

    def chainlist(self):
        """
        Get list of supported blockchain networks.

        Returns:
            list: Supported chains containing:
            - chainname: Network name (e.g., "Ethereum Mainnet")
            - chainid: Network ID (e.g., "1")
            - blockexplorer: Explorer URL
            - apiurl: API endpoint URL
            - status: Chain support status (1=active)

        Note:
            This method uses direct HTTP request instead of client
            as it's a meta-API endpoint
        """
        return requests.get(
            "https://api.etherscan.io/v2/chainlist",
            timeout=20
        ).json()['result']
