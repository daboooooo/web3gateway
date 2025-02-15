"""
Etherscan Accounts Module

This module provides functionality for account-related operations:
- Balance queries
- Transaction history
- Token transfers
- Mining history
"""


class Accounts:
    """
    Account-related API endpoint wrapper.

    Provides methods for querying account information including balances,
    transactions, and token transfers.

    Attributes:
        client: EtherScanV2 client instance for making API calls
    """

    def __init__(self, client):
        """
        Initialize Accounts endpoint wrapper.

        Args:
            client: EtherScanV2 client instance
        """
        self.client = client

    async def balance(self, address: str, tag: str = "latest"):
        """
        Get native token balance for an address.

        Args:
            address: Account address to query
            tag: Block parameter (latest/pending/earliest)

        Returns:
            Balance in Wei (smallest unit)
        """
        params = {"address": address, "tag": tag}
        return await self.client.request("account", "balance", params)

    async def balancemulti(self, addresses: list, tag: str = "latest"):
        """
        Get native token balance for multiple addresses.

        Args:
            addresses: List of account addresses to query
            tag: Block parameter (latest/pending/earliest)

        Returns:
            List of balances in Wei (smallest unit)
        """
        params = {"address": ",".join(addresses), "tag": tag}
        return await self.client.request("account", "balancemulti", params)

    async def txlist(self, address: str, startblock: int = 0, endblock: int = 99999999,
                     sort: str = 'asc'):
        """ Returns the list of transactions performed by an address. """
        params = {'address': address, 'startblock': startblock, 'endblock': endblock,
                  'sort': sort}
        return await self.client.request("account", "txlist", params)

    async def tokentx(self, address: str, contractaddress: str,
                      startblock: int = 0, endblock: int = 99999999, sort: str = 'asc'):
        """ Returns the list of ERC-20 token transfer events. """
        params = {'address': address, 'contractaddress': contractaddress,
                  'startblock': startblock, 'endblock': endblock, 'sort': sort}
        return await self.client.request("account", "tokentx", params)

    async def tokennfttx(self, address: str, contractaddress: str,
                         startblock: int = 0, endblock: int = 99999999, sort: str = 'asc'):
        """ Returns the list of ERC-721 token transfer events. """
        params = {'address': address, 'contractaddress': contractaddress,
                  'startblock': startblock, 'endblock': endblock, 'sort': sort}
        return await self.client.request("account", "tokennfttx", params)

    async def token1155tx(self, address: str, contractaddress: str,
                          startblock: int = 0, endblock: int = 99999999, sort: str = 'asc'):
        """ Returns the list of ERC-1155 token transfer events. """
        params = {'address': address, 'contractaddress': contractaddress,
                  'startblock': startblock, 'endblock': endblock, 'sort': sort}
        return await self.client.request("account", "token1155tx", params)

    async def txlistinternal(self, address: str, startblock: int = 0,
                             endblock: int = 99999999, page: int = 1,
                             offset: int = 10, sort: str = "desc"):
        """
        Get list of internal transactions for an address.

        Args:
            address: Account address
            startblock: Starting block number
            endblock: Ending block number
            page: Page number for results
            offset: Number of results per page
            sort: Sort order (asc/desc)

        Returns:
            List of internal transactions
        """
        params = {
            "address": address,
            "startblock": startblock,
            "endblock": endblock,
            "page": page,
            "offset": offset,
            "sort": sort
        }
        return await self.client.request("account", "txlistinternal", params)

    async def getminedblocks(self, address: str, blocktype: str = "blocks",
                             page: int = 1, offset: int = 10):
        """
        Get list of blocks mined by an address.

        Args:
            address: Miner address
            blocktype: Type of blocks (blocks/uncles)
            page: Page number for results
            offset: Number of results per page

        Returns:
            List of mined blocks
        """
        params = {
            "address": address,
            "blocktype": blocktype,
            "page": page,
            "offset": offset
        }
        return await self.client.request("account", "getminedblocks", params)
