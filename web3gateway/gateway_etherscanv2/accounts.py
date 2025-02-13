from . import EtherScanV2


class Accounts:
    """ https://docs.etherscan.io/etherscan-v2/api-endpoints/accounts
    """

    def __init__(self, etherscan: 'EtherScanV2'):
        self.etherscan = etherscan

    def balance(self, address: str, tag: str = 'latest'):
        """ Returns the Ether balance for a single address. """
        params = {'address': address, 'tag': tag}
        return self.etherscan.request("account", "balance", params)

    def balancemulti(self, address: str, tag: str = 'latest'):
        """ Returns the balance of multiple addresses in a single call. """
        params = {'address': address, 'tag': tag}
        return self.etherscan.request("account", "balancemulti", params)

    def txlist(self, address: str, startblock: int = 0, endblock: int = 99999999,
               sort: str = 'asc'):
        """ Returns the list of transactions performed by an address. """
        params = {'address': address, 'startblock': startblock, 'endblock': endblock,
                  'sort': sort}
        return self.etherscan.request("account", "txlist", params)

    def txlistinternal(self, address: str, startblock: int = 0, endblock: int = 99999999,
                       sort: str = 'asc'):
        """ Returns the list of internal transactions performed by an address. """
        params = {'address': address, 'startblock': startblock, 'endblock': endblock, 'sort': sort}
        return self.etherscan.request("account", "txlistinternal", params)

    def tokentx(self, address: str, contractaddress: str,
                startblock: int = 0, endblock: int = 99999999, sort: str = 'asc'):
        """ Returns the list of ERC-20 token transfer events. """
        params = {'address': address, 'contractaddress': contractaddress,
                  'startblock': startblock, 'endblock': endblock, 'sort': sort}
        return self.etherscan.request("account", "tokentx", params)

    def tokennfttx(self, address: str, contractaddress: str,
                   startblock: int = 0, endblock: int = 99999999, sort: str = 'asc'):
        """ Returns the list of ERC-721 token transfer events. """
        params = {'address': address, 'contractaddress': contractaddress,
                  'startblock': startblock, 'endblock': endblock, 'sort': sort}
        return self.etherscan.request("account", "tokennfttx", params)

    def token1155tx(self, address: str, contractaddress: str,
                    startblock: int = 0, endblock: int = 99999999, sort: str = 'asc'):
        """ Returns the list of ERC-1155 token transfer events. """
        params = {'address': address, 'contractaddress': contractaddress,
                  'startblock': startblock, 'endblock': endblock, 'sort': sort}
        return self.etherscan.request("account", "token1155tx", params)

    def getminedblocks(self, address: str, blocktype: str = 'blocks'):
        """ Returns the list of blocks mined by an address. """
        params = {'address': address, 'blocktype': blocktype}
        return self.etherscan.request("account", "getminedblocks", params)

    def txsbeaconwithdrawal(self, address: str, startblock: int = 0, endblock: int = 99999999,
                            sort: str = 'asc'):
        """ Returns the list of beacon chain withdrawals. """
        params = {'address': address, 'startblock': startblock, 'endblock': endblock, 'sort': sort}
        return self.etherscan.request("account", "txsBeaconWithdrawal", params)

    def balancehistory(self, address: str, blockno: int):
        """ Returns the balance history of an address at a specific block number. """
        params = {'address': address, 'blockno': blockno}
        return self.etherscan.request("account", "balancehistory", params)
