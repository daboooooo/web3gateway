from . import EtherScanV2


class ChainSpecific:

    def __init__(self, etherscan: 'EtherScanV2'):
        self.etherscan = etherscan

    def txnbridge(self, address: str):
        return self.etherscan.request("account", "txnbridge", {
            "address": address
        })
