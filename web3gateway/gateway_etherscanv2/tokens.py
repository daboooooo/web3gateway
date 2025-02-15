from typing import Optional

from . import EtherScanV2


class Tokens:
    """Token APIs from Etherscan
    https://docs.etherscan.io/etherscan-v2/api-endpoints/tokens
    """

    def __init__(self, etherscan: 'EtherScanV2'):
        self.etherscan = etherscan

    def tokensupply(self, contractaddress: str):
        """Returns the total supply of a specific ERC-20 token.

        Args:
            contractaddress: The contract address of the token

        Returns:
            Total supply in token's smallest unit
        """
        return self.etherscan.request(
            "stats", "tokensupply", {"contractaddress": contractaddress})

    def tokenbalance(self, contractaddress: str, address: str, tag: str = "latest"):
        """ Returns the current balance of an ERC-20 token of an address.

        Args:
            contractaddress: The contract address of the token
            address: The address to check balance for
            tag: Block number or 'latest'

        Returns:
            Token balance in token's smallest unit
        """
        return self.etherscan.request("account", "tokenbalance", {
            "contractaddress": contractaddress,
            "address": address,
            "tag": tag
        })

    def tokensupplyhistory(self, contractaddress: str, blockno: Optional[int] = None):
        """ [PRO] Returns the historical supply of a specific ERC-20 token.

        Args:
            contractaddress: The contract address of the token
            blockno: The block number to check supply for

        Returns:
            Historical supply in token's smallest unit
        """
        return self.etherscan.request("stats", "tokensupplyhistory", {
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
        return self.etherscan.request("account", "tokenbalancehistory", {
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
        return self.etherscan.request("token", "tokenholderlist", {
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
        return self.etherscan.request("token", "tokeninfo", {
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
        return self.etherscan.request("account", "addresstokenbalance", {
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
        return self.etherscan.request("account", "addresstokennftbalance", {
            "address": address
        })

    def addresstokennftinventory(self, address: str):
        """ [PRO] Returns the NFT inventory of an address.

        Args:
            address: The address to check inventory for

        Returns:
            NFT inventory
        """
        return self.etherscan.request("account", "addresstokennftinventory", {
            "address": address
        })
