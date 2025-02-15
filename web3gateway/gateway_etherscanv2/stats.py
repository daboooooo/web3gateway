from . import EtherScanV2


class Stats:
    """Statistics APIs from Etherscan
    https://docs.etherscan.io/etherscan-v2/api-endpoints/stats-1
    """

    def __init__(self, etherscan: 'EtherScanV2'):
        self.etherscan = etherscan

    def ethsupply(self):
        """Returns the current amount of Ether in circulation.

        Returns:
            Total supply in Wei
        """
        return self.etherscan.request("stats", "ethsupply", {})

    def ethsupply2(self, **params):
        """Returns the current amount of Ether in circulation, ETH2 Staking rewards,
        EIP1559 burnt fees, and total withdrawn ETH from the beacon chain.

        Returns:
            {
                "status":"1",
                "message":"OK",
                "result":{
                    "EthSupply":"122373866217800000000000000",
                    "Eth2Staking":"1157529105115885000000000",
                    "BurntFees":"3102505506455601519229842",
                    "WithdrawnTotal":"1170200333006131000000000"
                }
            }
        """
        return self.etherscan.request("stats", "ethsupply2", params)

    def ethprice(self):
        """Returns the latest ETH price and other market data.

        Returns:
            {
                "ethbtc": "0.068",
                "ethbtc_timestamp": "1684952881",
                "ethusd": "1842.31",
                "ethusd_timestamp": "1684952881"
            }
        """
        return self.etherscan.request("stats", "ethprice", {})

    def chainsize(self, startdate: str, enddate: str,
                  clienttype: str = "geth", syncmode: str = "default",
                  sort: str = "asc"):
        """Returns the daily size of the Ethereum blockchain.

        Args:
            startdate: Start date in yyyy-MM-dd format
            enddate: End date in yyyy-MM-dd format
            sort: Sort direction ('asc' or 'desc')

        Returns:
            [{
                "blockNumber":"7156164",
                "chainTimeStamp":"2019-02-01",
                "chainSize":"184726421279",
                "clientType":"Geth",
                "syncMode":"Default"
            }, ...]
        """
        return self.etherscan.request("stats", "chainsize", {
            'startdate': startdate,
            'enddate': enddate,
            'clienttype': clienttype,
            'syncmode': syncmode,
            'sort': sort
        })

    def nodecount(self):
        """Returns the total number of discoverable Ethereum nodes.

        Returns:
            {
                "TotalNodeCount": "8004",
                "LastUpdateTimestamp": "1688051234"
            }
        """
        return self.etherscan.request("stats", "nodecount", {})

    def dailytxnfee(self, startdate: str, enddate: str, sort: str = "asc"):
        """ [PRO] Returns the daily transaction fee in Wei.

        Args:
            startdate: Start date in yyyy-MM-dd format
            enddate: End date in yyyy-MM-dd format
            sort: Sort direction ('asc' or 'desc')

        Returns:
            [{
                "UTCDate": "2023-07-01",
                "unixTimeStamp": "1688169600",
                "transactionFee_Wei": "123456789000000000"
            }, ...]
        """
        return self.etherscan.request("stats", "dailytxnfee", {
            'startdate': startdate,
            'enddate': enddate,
            'sort': sort
        })

    def dailynewaddress(self, startdate: str, enddate: str, sort: str = "asc"):
        """ [PRO] Returns the number of new Ethereum addresses created per day.

        Args:
            startdate: Start date in yyyy-MM-dd format
            enddate: End date in yyyy-MM-dd format
            sort: Sort direction ('asc' or 'desc')

        Returns:
            [{
                "UTCDate": "2023-07-01",
                "unixTimeStamp": "1688169600",
                "newAddressCount": "12345"
            }, ...]
        """
        return self.etherscan.request("stats", "dailynewaddress", {
            'startdate': startdate,
            'enddate': enddate,
            'sort': sort
        })

    def dailynetutilization(self, startdate: str, enddate: str, sort: str = "asc"):
        """ [PRO] Returns the daily network utilization percentage.

        Args:
            startdate: Start date in yyyy-MM-dd format
            enddate: End date in yyyy-MM-dd format
            sort: Sort direction ('asc' or 'desc')

        Returns:
            [{
                "UTCDate": "2023-07-01",
                "unixTimeStamp": "1688169600",
                "networkUtilization": "68.45"
            }, ...]
        """
        return self.etherscan.request("stats", "dailynetutilization", {
            'startdate': startdate,
            'enddate': enddate,
            'sort': sort
        })

    def dailyavghashrate(self, **params):
        """ [PRO] Returns the daily average hash rate."""
        return self.etherscan.request("stats", "dailyavghashrate", params)

    def dailytx(self, **params):
        """ [PRO] Returns the daily number of transactions."""
        return self.etherscan.request("stats", "dailytx", params)

    def dailyavgnetdifficulty(self, **params):
        """  [PRO] Returns the daily average network difficulty."""
        return self.etherscan.request("stats", "dailyavgnetdifficulty", params)

    def ethdailymarketcap(self, **params):
        """ [PRO] Returns the daily market cap of Ethereum."""
        return self.etherscan.request("stats", "ethdailymarketcap", params)

    def ethdailyprice(self, **params):
        """ [PRO] Returns the daily price of Ethereum."""
        return self.etherscan.request("stats", "ethdailyprice", params)
