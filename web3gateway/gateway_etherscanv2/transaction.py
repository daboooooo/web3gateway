from . import EtherScanV2


class Transaction:
    """Transaction APIs from Etherscan
    https://docs.etherscan.io/etherscan-v2/api-endpoints/stats
    """

    def __init__(self, etherscan: 'EtherScanV2'):
        self.etherscan = etherscan

    def getstatus(self, txhash: str):
        """Returns the status of a specific transaction.

        Args:
            txhash: Transaction hash

        Returns:
            {
                "isError":"1",
                "errDescription":"Bad jump destination"
            }
        """
        return self.etherscan.request("transaction", "getstatus", {"txhash": txhash})

    def gettxreceiptstatus(self, txhash: str):
        """Returns the receipt status of a specific transaction.

        Args:
            txhash: Transaction hash

        Returns:
            {
                "status": "1" // 1 = Success, 0 = Fail
            }
        """
        return self.etherscan.request("transaction", "gettxreceiptstatus", {"txhash": txhash})
