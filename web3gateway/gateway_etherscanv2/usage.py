import requests

from . import EtherScanV2


class Usage:

    def __init__(self, etherscan: 'EtherScanV2'):
        self.etherscan = etherscan

    def getapilimit(self, **params):
        return self.etherscan.request("getapilimit", "getapilimit", params)

    def chainlist(self):
        return requests.get("https://api.etherscan.io/v2/chainlist", timeout=20).json()['result']
