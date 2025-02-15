import requests

from . import EtherScanV2


class Usage:

    def __init__(self, etherscan: 'EtherScanV2'):
        self.etherscan = etherscan

    def getapilimit(self):
        """Returns the API limit information.

        Returns:
            {
                "creditsUsed":207,
                "creditsAvailable":499793,
                "creditLimit":500000,
                "limitInterval":"daily",
                "intervalExpiryTimespan":"07:20:05"
            }
        """
        return self.etherscan.request("getapilimit", "getapilimit", {})

    def chainlist(self):
        """ Returns the list of supported blockchains.

        Returns:
            [
                {
                    "chainname":"Ethereum Mainnet",
                    "chainid":"1",
                    "blockexplorer":"https://etherscan.io",
                    "apiurl":"https://api.etherscan.io/v2/api?chainid=1",
                    "status":1
                },...
            ]
        """
        return requests.get("https://api.etherscan.io/v2/chainlist", timeout=20).json()['result']
