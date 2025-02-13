from . import EtherScanV2


class Contracts:

    def __init__(self, etherscan: 'EtherScanV2'):
        self.etherscan = etherscan

    def getabi(self, **params):
        return self.etherscan.request("contract", "getabi", params)

    def getsourcecode(self, **params):
        return self.etherscan.request("contract", "getsourcecode", params)

    def getcontractcreation(self, **params):
        return self.etherscan.request("contract", "getcontractcreation", params)

    def verifysourcecode(self, **params):
        return self.etherscan.request("contract", "verifysourcecode", params)

    def checkverifystatus(self, **params):
        return self.etherscan.request("contract", "checkverifystatus", params)

    def verifyproxycontract(self, **params):
        # ⚠️ ONLY POST METHOD ⚠️
        return self.etherscan.request("contract", "verifyproxycontract", params)

    def checkproxyverification(self, **params):
        return self.etherscan.request("contract", "checkproxyverification", params)
