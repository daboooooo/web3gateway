from . import EtherScanV2


class GasTracker:

    def __init__(self, etherscan: 'EtherScanV2'):
        self.etherscan = etherscan

    def gasestimate(self, gasprice: int):
        return self.etherscan.request("gastracker", "gasestimate", {'gasprice': gasprice})

    def gasoracle(self):
        return self.etherscan.request("gastracker", "gasoracle", {})

    def dailyavggaslimit(self, startdate: str, enddate: str, sort: str = 'asc'):
        """ [PRO] Returns the historical daily average gas limit of the Ethereum network.

        Params:
            startdate 2019-02-01
            enddate 2019-02-28
            sort

        Returns:
            {
                "status":"1",
                "message":"OK",
                "result":[
                    {
                        "UTCDate":"2019-02-01",
                        "unixTimeStamp":"1548979200",
                        "gasLimit":"8001360"
                    },
                    {
                        "UTCDate":"2019-02-27",
                        "unixTimeStamp":"1551225600",
                        "gasLimit":"8001071"
                    },
                    {
                        "UTCDate":"2019-02-28",
                        "unixTimeStamp":"1551312000",
                        "gasLimit":"8001137"
                    }
                ]
            }
        """
        return self.etherscan.request(
            "stats", "dailyavggaslimit",
            {
                'startdate': startdate,
                'enddate': enddate,
                'sort': sort
            })

    def dailygasused(self, **params):
        """ [PRO] """
        return self.etherscan.request("stats", "dailygasused", params)

    def dailyavggasprice(self, **params):
        """ [PRO] """
        return self.etherscan.request("stats", "dailyavggasprice", params)
