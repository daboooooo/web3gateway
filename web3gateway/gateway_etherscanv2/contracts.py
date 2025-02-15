from . import EtherScanV2


class Contracts:
    """Contract APIs from Etherscan
    https://docs.etherscan.io/etherscan-v2/api-endpoints/contracts
    """

    def __init__(self, etherscan: 'EtherScanV2'):
        self.etherscan = etherscan

    def getabi(self, address: str):
        """Returns the contract ABI for given contract address.

        Args:
            address: Contract address

        Returns:
            Contract ABI as JSON string
        """
        return self.etherscan.request("contract", "getabi", {'address': address})

    def getsourcecode(self, address: str):
        """Returns the Solidity source code of a verified smart contract.

        Args:
            address: Contract address

        Returns:
            List containing contract details including source code
        """
        return self.etherscan.request("contract", "getsourcecode", {'address': address})

    def getcontractcreation(self, contractaddresses: str):
        """Returns a contract's deployer address and transaction hash it was created.

        Args:
            contractaddresses: Comma separated list of contract addresses

        Returns:
            List of contract creation details
        """
        return self.etherscan.request("contract", "getcontractcreation",
                                      {'contractaddresses': contractaddresses})

    def verifysourcecode(self, **params):
        """Verifies contract source code. Requires multiple parameters.

        Returns:
            GUID for checking verification status
        """
        return self.etherscan.request("contract", "verifysourcecode", params)

    def checkverifystatus(self, guid: str):
        """Returns the verification status of a contract.

        Args:
            guid: The GUID from verifysourcecode

        Returns:
            Verification status
        """
        return self.etherscan.request("contract", "checkverifystatus", {'guid': guid})

    def verifyproxycontract(self, **params):
        """Submits a contract verification request for proxy contracts.

        Returns:
            GUID for checking verification status
        """
        return self.etherscan.request("contract", "verifyproxycontract", params)

    def checkproxyverification(self, guid: str):
        """Returns the verification status of a proxy contract.

        Args:
            guid: The GUID from verifyproxycontract

        Returns:
            Verification status
        """
        return self.etherscan.request("contract", "checkproxyverification", {'guid': guid})
