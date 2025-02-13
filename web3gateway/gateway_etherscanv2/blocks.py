from . import EtherScanV2


class Blocks:

    def __init__(self, etherscan: 'EtherScanV2'):
        self.etherscan = etherscan

    def getblockreward(self, **params):
        return self.etherscan.request("block", "getblockreward", params)

    def getblockcountdown(self, **params):
        return self.etherscan.request("block", "getblockcountdown", params)

    def getblocknobytime(self, **params):
        return self.etherscan.request("block", "getblocknobytime", params)

    def dailyavgblocksize(self, **params):
        return self.etherscan.request("stats", "dailyavgblocksize", params)

    def dailyblkcount(self, **params):
        return self.etherscan.request("stats", "dailyblkcount", params)

    def dailyblockrewards(self, **params):
        return self.etherscan.request("stats", "dailyblockrewards", params)

    def dailyavgblocktime(self, **params):
        return self.etherscan.request("stats", "dailyavgblocktime", params)

    def dailyuncleblkcount(self, **params):
        return self.etherscan.request("stats", "dailyuncleblkcount", params)
