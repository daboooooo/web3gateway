from . import EtherScanV2


class Logs:

    def __init__(self, etherscan: 'EtherScanV2'):
        self.etherscan = etherscan

    def getLogs(self, **params):
        return self.etherscan.request("logs", "getLogs", params)
