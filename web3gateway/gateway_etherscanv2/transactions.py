from . import EtherScanV2


class Transactions:

    def __init__(self, etherscan: 'EtherScanV2'):
        self.etherscan = etherscan

    def getstatus(self, **params):
        return self.etherscan.request("transaction", "getstatus", params)

    def gettxreceiptstatus(self, **params):
        return self.etherscan.request("transaction", "gettxreceiptstatus", params)
