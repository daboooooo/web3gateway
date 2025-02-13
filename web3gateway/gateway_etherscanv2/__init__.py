import json
from urllib.parse import urlencode

import requests

from web3gateway.utils.cache import CacheService
from web3gateway.utils.rate_limiter import RateLimiter

from .metadata import valid_params


CHAINLIST_URL = "https://api.etherscan.io/v2/chainlist"


class EtherScanV2:

    def __init__(self, config: dict) -> None:
        self._supported_chains: list[dict] = []
        self.update_supported_chains()

        self.config = config
        self.rate_limiter = RateLimiter(config)

        self.cache = CacheService(self.config['redis_url'])

        self.cached_chain_info: dict[int, dict] = {}
        self._base_url_with_chainid: str = ""
        self.chain_name: str = ""
        self.chain_id: int = 0

        # import submodules to avoid circular imports
        from .accounts import Accounts
        from .blocks import Blocks
        from .chainspecific import ChainSpecific
        from .contracts import Contracts
        from .gastracker import GasTracker
        from .logs import Logs
        from .proxies import Proxy
        from .stats import Stats
        from .tokens import Tokens
        from .transactions import Transactions
        from .usage import Usage

        self.account = Accounts(self)
        self.contract = Contracts(self)
        self.transaction = Transactions(self)
        self.block = Blocks(self)
        self.logs = Logs(self)
        self.proxy = Proxy(self)
        self.tokens = Tokens(self)
        self.gas_tracker = GasTracker(self)
        self.stats = Stats(self)
        self.chain_specific = ChainSpecific(self)
        self.usage = Usage(self)

    def set_chain_id(self, chainid: int):
        """ set chain id before making requests """
        # chain info data structure
        # {
        #     "chainname": "Ethereum Mainnet",
        #     "chainid": "1",
        #     "blockexplorer": "https://etherscan.io",
        #     "apiurl": "https://api.etherscan.io/v2/api?chainid=1",
        #     "status": 1,
        #     "comment": ""
        # }
        if chainid not in self.cached_chain_info:
            chain_info = next(
                (chain for chain in self._supported_chains if chain['chainid'] == str(chainid)),
                None)
            if chain_info is None:
                raise ValueError(f"Chain id {chainid} is not supported.")
            self.cached_chain_info[chainid] = chain_info
        else:
            chain_info = self.cached_chain_info[chainid]

        self._base_url_with_chainid = chain_info['apiurl']
        self.chain_name = chain_info['chainname']
        self.chain_id = chainid

        print(f"{self.chain_name} (id: {self.chain_id}) "
              f"etherscan api url: {self._base_url_with_chainid}")

    async def request(self, module: str, action: str, params: dict):
        await self.rate_limiter.acquire()

        # 构建缓存key
        cache_key = f"etherscanv2:{self.chain_id}:{module}:{action}:" + \
            f"{json.dumps(params, sort_keys=True)}"

        # 尝试从缓存获取数据
        cached_result = await self.cache.get(cache_key)
        if cached_result is not None:
            return cached_result

        # 如果缓存未命中，则请求API
        api_params = {k: v for k, v in params.items() if k in valid_params[action]}
        url = f"{self._base_url_with_chainid}&" + \
            f"apikey={self.config['etherscan_api_key']}&" + \
            f"module={module}&action={action}&{urlencode(api_params)}"
        print(f"Requesting Etherscan url: {url}")
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            raise OSError(f"Failed to get Etherscan url: {url}")
        res_dict = res.json()
        if res_dict['status'] == '0' or res_dict['message'] == 'NOTOK':
            raise ValueError(res_dict['result'])

        # 将结果存入缓存
        await self.cache.set(cache_key, res_dict['result'], expire=self.config['cache_expiration'])
        return res_dict['result']

    def update_supported_chains(self):
        """ update supported chains """
        res = requests.get(CHAINLIST_URL, timeout=10)
        if res.status_code != 200:
            raise OSError("Failed to fetch supported chains.")
        res_dict = res.json()
        # check if the request is successful
        if 'totalcount' not in res_dict:
            raise ValueError("Failed to fetch supported chains.")
        print(f"Etherscan V2 supported chains: {res_dict['totalcount']}")
        self._supported_chains = res_dict['result']

    @classmethod
    async def create(cls, config: dict):
        """
        工厂方法：创建并初始化 EtherScanV2 实例
        """
        instance = cls(config)
        # 初始化缓存服务
        await instance.cache.initialize()
        return instance
