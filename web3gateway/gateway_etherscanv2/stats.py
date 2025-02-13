from . import EtherScanV2


class Stats:

    def __init__(self, etherscan: 'EtherScanV2'):
        self.etherscan = etherscan

    def ethsupply(self, **params):
        return self.etherscan.request("stats", "ethsupply", params)

    def ethsupply2(self, **params):
        return self.etherscan.request("stats", "ethsupply2", params)

    def ethprice(self, **params):
        return self.etherscan.request("stats", "ethprice", params)

    def chainsize(self, **params):
        return self.etherscan.request("stats", "chainsize", params)

    def nodecount(self, **params):
        return self.etherscan.request("stats", "nodecount", params)

    def dailytxnfee(self, **params):
        return self.etherscan.request("stats", "dailytxnfee", params)

    def dailynewaddress(self, **params):
        return self.etherscan.request("stats", "dailynewaddress", params)

    def dailynetutilization(self, **params):
        return self.etherscan.request("stats", "dailynetutilization", params)

    def dailyavghashrate(self, **params):
        return self.etherscan.request("stats", "dailyavghashrate", params)

    def dailytx(self, **params):
        return self.etherscan.request("stats", "dailytx", params)

    def dailyavgnetdifficulty(self, **params):
        return self.etherscan.request("stats", "dailyavgnetdifficulty", params)

    def ethdailymarketcap(self, **params):
        return self.etherscan.request("stats", "ethdailymarketcap", params)

    def ethdailyprice(self, **params):
        return self.etherscan.request("stats", "ethdailyprice", params)
