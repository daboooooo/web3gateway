"""
Etherscan Transaction Module

This module provides functionality for transaction-related operations:
- Transaction status queries
- Receipt status verification
- Transaction error information
"""


class Transaction:
    """
    Transaction-related API endpoint wrapper.

    Provides methods for querying transaction statuses and receipts,
    with detailed error information when available.

    Attributes:
        client: EtherScanV2 client instance for making API calls
    """

    def __init__(self, client):
        """
        Initialize Transaction endpoint wrapper.

        Args:
            client: EtherScanV2 client instance
        """
        self.client = client

    def getstatus(self, txhash: str):
        """
        Get detailed status of a transaction including error information.

        Args:
            txhash: Transaction hash to query

        Returns:
            dict: Transaction status containing:
            - isError: "0" for success, "1" for failure
            - errDescription: Error message if failed
                (e.g., "Bad jump destination", "Out of gas")

        Note:
            This endpoint provides more detailed error information
            compared to gettxreceiptstatus
        """
        return self.client.request("transaction", "getstatus", {"txhash": txhash})

    def gettxreceiptstatus(self, txhash: str):
        """
        Get basic receipt status of a transaction.

        Args:
            txhash: Transaction hash to query

        Returns:
            dict: Receipt status containing:
            - status: "1" for success, "0" for failure

        Note:
            This is a lighter-weight call compared to getstatus,
            useful when only success/failure information is needed
        """
        return self.client.request("transaction", "gettxreceiptstatus", {"txhash": txhash})
