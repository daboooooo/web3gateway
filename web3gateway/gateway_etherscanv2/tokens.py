from . import EtherScanV2


class Tokens:

    def __init__(self, etherscan: 'EtherScanV2'):
        self.etherscan = etherscan

    def tokensupply(self, **params):
        return self.etherscan.request("stats", "tokensupply", params)

    def tokenbalance(self, contractaddress: str, address: str, tag: str = "latest"):
        return self.etherscan.request("account", "tokenbalance", {
            "contractaddress": contractaddress,
            "address": address,
            "tag": tag
        })

    def tokensupplyhistory(self, **params):
        return self.etherscan.request("stats", "tokensupplyhistory", params)

    def tokenbalancehistory(self, **params):
        return self.etherscan.request("account", "tokenbalancehistory", params)

    def tokenholderlist(self, **params):
        return self.etherscan.request("token", "tokenholderlist", params)

    def tokeninfo(self, **params):
        return self.etherscan.request("token", "tokeninfo", params)

    def addresstokenbalance(self, **params):
        return self.etherscan.request("account", "addresstokenbalance", params)

    def addresstokennftbalance(self, **params):
        return self.etherscan.request("account", "addresstokennftbalance", params)

    def addresstokennftinventory(self, **params):
        return self.etherscan.request("account", "addresstokennftinventory", params)
