"""
Step 1: start web3gateway server
$ web3gateway

Step 2: run the tests
$ python tests/test_api.py
"""

import logging

import requests
from requests.auth import HTTPBasicAuth


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Web3GatewayTester:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.auth = HTTPBasicAuth("test_user", "test_password")
        self.test_address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
        self.test_token_address = "0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359"
        self.chain_id = 1

    def test_ping(self):
        """测试健康检查接口"""
        logger.info("Testing /ping endpoint...")
        response = requests.get(f"{self.base_url}/ping", timeout=10)
        assert response.status_code == 200
        logger.info(f"Ping response: {response.json()}")

    def test_assemble_transaction(self):
        """测试交易组装接口"""
        logger.info("Testing transaction assembly...")
        payload = {
            "chain_id": self.chain_id,
            "tx_params": {
                "from": self.test_address,
                "to": self.test_address,
                "value": "1000000000000000"
            },
            "gas_level": "fast"
        }
        response = requests.post(
            f"{self.base_url}/transaction/assemble",
            json=payload,
            auth=self.auth,
            timeout=10
        )
        assert response.status_code == 200
        logger.info(f"Assembly response: {response.json()}")
        return response.json()

    def test_get_balance(self):
        """测试获取余额接口"""
        logger.info("Testing balance query...")
        payload = {
            "chain_id": self.chain_id,
            "address": self.test_address
        }
        response = requests.post(
            f"{self.base_url}/account/balance",
            json=payload,
            auth=self.auth,
            timeout=10
        )
        assert response.status_code == 200
        logger.info(f"Balance response: {response.json()}")

    def test_get_token_balance(self):
        """测试获取代币余额接口"""
        logger.info("Testing token balance query...")
        payload = {
            "chain_id": self.chain_id,
            "contractaddress": self.test_token_address,
            "address": self.test_address
        }
        response = requests.post(
            f"{self.base_url}/account/token_balance",
            json=payload,
            auth=self.auth,
            timeout=10
        )
        assert response.status_code == 200
        logger.info(f"Token balance response: {response.json()}")

    def test_get_transactions(self):
        """测试获取交易列表接口"""
        logger.info("Testing transaction list query...")
        payload = {
            "chain_id": self.chain_id,
            "address": self.test_address
        }
        response = requests.post(
            f"{self.base_url}/account/txlist",
            json=payload,
            auth=self.auth,
            timeout=10
        )
        assert response.status_code == 200
        logger.info(f"Transaction list response: {response.json()}")

    def test_get_transaction_receipt(self):
        """测试获取交易收据接口"""
        logger.info("Testing transaction receipt query...")
        # 这里需要一个有效的交易哈希
        tx_hash = "0x123...your_transaction_hash"
        payload = {
            "chain_id": self.chain_id,
            "tx_hash": tx_hash
        }
        response = requests.post(
            f"{self.base_url}/transaction/get_receipt",
            json=payload,
            auth=self.auth,
            timeout=10
        )
        assert response.status_code == 200
        logger.info(f"Transaction receipt response: {response.json()}")

    def run_all_tests(self):
        """运行所有测试"""
        try:
            self.test_ping()
            self.test_get_balance()
            self.test_get_token_balance()
            self.test_get_transactions()
            self.test_assemble_transaction()
            # self.test_get_transaction_receipt()  # 需要有效的交易哈希才能测试
            logger.info("All tests completed successfully!")
        except Exception as e:
            logger.error(f"Test failed: {str(e)}")
            raise


if __name__ == "__main__":
    tester = Web3GatewayTester()
    tester.run_all_tests()
