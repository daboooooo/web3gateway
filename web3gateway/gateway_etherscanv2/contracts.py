"""
Etherscan Contracts Module

This module provides functionality for smart contract operations:
- Contract ABI retrieval
- Source code verification
- Contract creation information
- Proxy contract verification
"""


class Contracts:
    """
    Contract-related API endpoint wrapper.

    Provides methods for interacting with smart contracts including
    verification, source code retrieval, and deployment information.

    Attributes:
        client: EtherScanV2 client instance for making API calls
    """

    def __init__(self, client):
        """
        Initialize Contracts endpoint wrapper.

        Args:
            client: EtherScanV2 client instance
        """
        self.client = client

    def getabi(self, address: str):
        """
        Get the ABI for a verified smart contract.

        Args:
            address: Contract address to query

        Returns:
            Contract ABI as JSON string

        Note:
            Contract must be verified on Etherscan
        """
        return self.client.request("contract", "getabi", {'address': address})

    def getsourcecode(self, address: str):
        """
        Get the source code of a verified smart contract.

        Args:
            address: Contract address to query

        Returns:
            List containing contract details including:
            - Source code
            - ABI
            - Construction arguments
            - Compiler version
        """
        return self.client.request("contract", "getsourcecode", {'address': address})

    def getcontractcreation(self, contractaddresses: str):
        """
        Get contract creator address and creation transaction.

        Args:
            contractaddresses: Comma separated list of contract addresses

        Returns:
            List of contract creation details including:
            - Creator address
            - Creation transaction hash
            - Timestamp
        """
        return self.client.request("contract", "getcontractcreation",
                                   {'contractaddresses': contractaddresses})

    def verifysourcecode(self, **params):
        """
        Submit contract source code for verification.

        Args:
            **params: Contract verification parameters including:
                - sourceCode: Contract source code
                - contractAddress: Address to verify
                - compilerVersion: Solidity version
                - optimizationUsed: Optimization flag
                - constructorArguments: Constructor args (if any)

        Returns:
            GUID: Verification request identifier

        Note:
            Use checkverifystatus to monitor verification progress
        """
        return self.client.request("contract", "verifysourcecode", params)

    def checkverifystatus(self, guid: str):
        """
        Check status of a contract verification request.

        Args:
            guid: Verification request identifier

        Returns:
            Verification status:
            - 'Pending' - In progress
            - 'Pass' - Successful
            - 'Fail' - Failed with reason
        """
        return self.client.request("contract", "checkverifystatus", {'guid': guid})

    def verifyproxycontract(self, **params):
        """
        Submit proxy contract for verification.

        Args:
            **params: Proxy verification parameters including:
                - address: Proxy contract address
                - expectedImplementation: Implementation address
                - constructorArguments: Constructor args (if any)

        Returns:
            GUID: Verification request identifier
        """
        return self.client.request("contract", "verifyproxycontract", params)

    def checkproxyverification(self, guid: str):
        """
        Check status of a proxy contract verification.

        Args:
            guid: Verification request identifier

        Returns:
            Proxy verification status:
            - 'Pending' - In progress
            - 'Pass' - Successful
            - 'Fail' - Failed with reason
        """
        return self.client.request("contract", "checkproxyverification", {'guid': guid})
