"""
Etherscan Token Operations Module

This module provides functionality for interacting with ERC20 and ERC721 tokens:
- Token balance queries
- Token supply information
- Token transfer events
"""
from typing import Optional


class Tokens:
    """
    Token-related API endpoint wrapper.

    Provides methods for querying token balances, supplies, and transfers
    across different token standards (ERC20, ERC721).

    Attributes:
        client: EtherScanV2 client instance for making API calls
    """

    def __init__(self, client):
        """
        Initialize Tokens endpoint wrapper.

        Args:
            client: EtherScanV2 client instance
        """
        self.client = client

    async def tokenbalance(self, contractaddress: str, address: str, tag: str = "latest"):
        """
        Get token balance for an address.

        Args:
            contractaddress: Token contract address
            address: Account address to query
            tag: Block parameter (latest/pending/earliest)

        Returns:
            Token balance in smallest decimal representation
        """
        params = {
            "contractaddress": contractaddress,
            "address": address,
            "tag": tag
        }
        return await self.client.request("account", "tokenbalance", params)

    async def tokensupply(self, contractaddress: str):
        """
        Get total supply of a token.

        Args:
            contractaddress: Token contract address

        Returns:
            Total token supply in smallest decimal representation
        """
        params = {"contractaddress": contractaddress}
        return await self.client.request("stats", "tokensupply", params)

    def tokensupplyhistory(self, contractaddress: str, blockno: Optional[int] = None):
        """ [PRO] Returns the historical supply of a specific ERC-20 token.

        Args:
            contractaddress: The contract address of the token
            blockno: The block number to check supply for

        Returns:
            Historical supply in token's smallest unit
        """
        return self.client.request("stats", "tokensupplyhistory", {
            "contractaddress": contractaddress,
            "blockno": blockno
        })

    def tokenbalancehistory(self, contractaddress: str, address: str,
                            blockno: Optional[int] = None):
        """ [PRO] Returns the historical balance of an ERC-20 token of an address.

        Args:
            contractaddress: The contract address of the token
            address: The address to check balance for
            blockno: The block number to check balance for

        Returns:
            Historical balance in token's smallest unit
        """
        return self.client.request("account", "tokenbalancehistory", {
            "contractaddress": contractaddress,
            "address": address,
            "blockno": blockno
        })

    def tokenholderlist(self, contractaddress: str,
                        page: Optional[int] = None, offset: Optional[int] = None):
        """ [PRO] Returns the list of token holders of a specific ERC-20 token.

        Args:
            contractaddress: The contract address of the token
            page: The page number to fetch
            offset: The number of records per page

        Returns:
            List of token holders
        """
        return self.client.request("token", "tokenholderlist", {
            "contractaddress": contractaddress,
            "page": page,
            "offset": offset
        })

    def tokeninfo(self, contractaddress: str):
        """ [PRO] Returns the information of a specific ERC-20 token.

        Args:
            contractaddress: The contract address of the token

        Returns:
            Token information
        """
        return self.client.request("token", "tokeninfo", {
            "contractaddress": contractaddress
        })

    def addresstokenbalance(self, address: str, contractaddress: Optional[str] = None):
        """ [PRO] Returns the token balance of an address.

        Args:
            address: The address to check balance for
            contractaddress: The contract address of the token (optional)

        Returns:
            Token balance in token's smallest unit
        """
        return self.client.request("account", "addresstokenbalance", {
            "address": address,
            "contractaddress": contractaddress
        })

    def addresstokennftbalance(self, address: str):
        """ [PRO] Returns the NFT balance of an address.

        Args:
            address: The address to check balance for

        Returns:
            NFT balance
        """
        return self.client.request("account", "addresstokennftbalance", {
            "address": address
        })

    def addresstokennftinventory(self, address: str):
        """ [PRO] Returns the NFT inventory of an address.

        Args:
            address: The address to check inventory for

        Returns:
            NFT inventory
        """
        return self.client.request("account", "addresstokennftinventory", {
            "address": address
        })
