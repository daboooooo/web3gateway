"""
Etherscan API V2 Client Module

This module provides a comprehensive wrapper for the Etherscan V2 API with:
- Multi-chain support via chainlist API
- Rate limiting for API calls
- Redis-based caching
- Modular organization of API endpoints
"""

import json
from urllib.parse import urlencode

import requests

from web3gateway.utils.cache import CacheService
from web3gateway.utils.rate_limiter import RateLimiter

from .metadata import valid_params


CHAINLIST_URL = "https://api.etherscan.io/v2/chainlist"


class EtherScanV2:
    """
    Etherscan V2 API client with multi-chain support.

    This class provides a comprehensive interface to the Etherscan V2 API
    with built-in caching, rate limiting, and chain management.

    Attributes:
        config (dict): Configuration parameters
        cache (CacheService): Redis cache instance
        rate_limiter (RateLimiter): Rate limiting service
        chain_id (int): Currently selected chain ID
        chain_name (str): Currently selected chain name

    Example:
        client = await EtherScanV2.create(config)
        client.set_chain_id(1)  # Select Ethereum mainnet
        balance = await client.account.balance("0x...")
    """

    def __init__(self, config: dict) -> None:
        """
        Initialize EtherScanV2 client.

        Args:
            config: Configuration dictionary containing:
                - redis_url: Redis connection string
                - etherscan_api_key: Etherscan API key
                - rate_limit settings
                - cache_expiration settings
        """
        self._supported_chains: list[dict] = []
        self.update_supported_chains()

        self.config = config
        self.rate_limiter = RateLimiter(config)
        self.cache = CacheService(self.config['redis_url'])

        self.cached_chain_info: dict[int, dict] = {}
        self._base_url_with_chainid: str = ""
        self.chain_name: str = ""
        self.chain_id: int = 0

        # Initialize API modules
        from .accounts import Accounts
        from .blocks import Blocks
        from .chainspecific import ChainSpecific
        from .contracts import Contracts
        from .gastracker import GasTracker
        from .geth_proxy import Proxy
        from .logs import Logs
        from .stats import Stats
        from .tokens import Tokens
        from .transaction import Transaction
        from .usage import Usage

        # Create API module instances
        self.account = Accounts(self)
        self.contract = Contracts(self)
        self.transaction = Transaction(self)
        self.block = Blocks(self)
        self.logs = Logs(self)
        self.proxy = Proxy(self)
        self.tokens = Tokens(self)
        self.gas_tracker = GasTracker(self)
        self.stats = Stats(self)
        self.chain_specific = ChainSpecific(self)
        self.usage = Usage(self)

    def set_chain_id(self, chainid: int):
        """
        Set active chain for subsequent API calls.

        Args:
            chainid: Chain ID to use (e.g., 1 for Ethereum mainnet)

        Raises:
            ValueError: If chain ID is not supported
        """
        # Look up chain info in cache first
        if chainid not in self.cached_chain_info:
            chain_info = next(
                (chain for chain in self._supported_chains if chain['chainid'] == str(chainid)),
                None)
            if chain_info is None:
                raise ValueError(f"Chain id {chainid} is not supported.")
            self.cached_chain_info[chainid] = chain_info
        else:
            chain_info = self.cached_chain_info[chainid]

        # Update instance attributes for selected chain
        self._base_url_with_chainid = chain_info['apiurl']
        self.chain_name = chain_info['chainname']
        self.chain_id = chainid

        print(f"{self.chain_name} (id: {self.chain_id}) "
              f"etherscan api url: {self._base_url_with_chainid}")

    async def request(self, module: str, action: str, params: dict):
        """
        Make an API request with caching and rate limiting.

        Args:
            module: API module name
            action: API action name
            params: Request parameters

        Returns:
            API response data

        Raises:
            OSError: If API request fails
            ValueError: If API returns error response
        """
        # Apply rate limiting
        await self.rate_limiter.acquire()

        # Generate cache key
        cache_key = f"etherscanv2:{self.chain_id}:{module}:{action}:" + \
            f"{json.dumps(params, sort_keys=True)}"

        # Try cache first
        cached_result = await self.cache.get(cache_key)
        if cached_result is not None:
            return cached_result

        # Build API request URL with validated parameters
        api_params = {k: v for k, v in params.items() if k in valid_params[action]}
        url = f"{self._base_url_with_chainid}&" + \
            f"apikey={self.config['etherscan_api_key']}&" + \
            f"module={module}&action={action}&{urlencode(api_params)}"

        # Make API request
        print(f"Requesting Etherscan url: {url}")
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            raise OSError(f"Failed to get Etherscan url: {url}")

        # Parse and validate response
        res_dict = res.json()
        if 'status' in res_dict:
            if res_dict['status'] == '0' or res_dict['message'] == 'NOTOK':
                print(res_dict)
                raise ValueError(res_dict['result'])
        elif 'jsonrpc' in res_dict:
            if res_dict['jsonrpc'] != '2.0':
                raise ValueError("Unknown jsonrpc version")

        # Cache successful response
        await self.cache.set(cache_key, res_dict['result'],
                             expire=self.config['cache_expiration'])
        return res_dict['result']

    def update_supported_chains(self):
        """
        Update list of supported chains from Etherscan API.

        Raises:
            OSError: If chainlist request fails
            ValueError: If response format is invalid
        """
        res = requests.get(CHAINLIST_URL, timeout=10)
        if res.status_code != 200:
            raise OSError("Failed to fetch supported chains.")
        res_dict = res.json()
        if 'totalcount' not in res_dict:
            raise ValueError("Failed to fetch supported chains.")
        print(f"Etherscan V2 supported chains: {res_dict['totalcount']}")
        self._supported_chains = res_dict['result']

    @classmethod
    async def create(cls, config: dict):
        """
        Factory method to create and initialize EtherScanV2 instance.

        Args:
            config: Configuration dictionary

        Returns:
            Initialized EtherScanV2 instance
        """
        instance = cls(config)
        await instance.cache.initialize()
        return instance
