from urllib.parse import urlencode
from .accounts import Accounts
from .contracts import Contracts
from .transactions import Transactions
from .blocks import Blocks
from .logs import Logs
from .proxys import Proxy
from .tokens import Tokens
from .gastracker import GasTracker
from .stats import Stats
from .chainspecific import ChainSpecific
from .usage import Usage
from .metadata import *
import requests


__all__ = ["EtherScanV2"]

CHAINLIST_URL = "https://api.etherscan.io/v2/chainlist"


class EtherScanV2:
    def __init__(self, apikey: str, chainid=int) -> None:
        self._cached_supported_chains = []
        self.update_supported_chains()
        print(f"There are {len(self._cached_supported_chains)} supported chains.")

        # find chain info item in supported_chains according with chainid
        chain_info = next((chain for chain in self.supported_chains if chain['id'] == str(chainid)), None)
        if chain_info is None:
            raise Exception(f"Chain id {chainid} is not supported.")

        self.__base_url_with_chainid: str = chain_info['apiurl']
        print(f"Base URL with ChainID: {self.__base_url_with_chainid}")
        
        self.api_key: str = apikey
        self.chain_id: int = chainid
        self.__valid_params = valid_params

        self.Account = Accounts(self)
        self.Contract = Contracts(self)
        self.Transaction = Transactions(self)
        self.Block = Blocks(self)
        self.Logs = Logs(self)
        self.Proxy = Proxy(self)
        self.Tokens = Tokens(self)
        self.GasTracker = GasTracker(self)
        self.Stats = Stats(self)
        self.ChainSpecific = ChainSpecific(self)
        self.Usage = Usage(self)
        
        self.connect()

    def __connect_api(self, module: str, action: str, params: dict):
        api_params = {k: v for k, v in params.items() if k in self.__valid_params[action]}
        url = f"{self.__base_url_with_chainid}&apikey={self.api_key}&module={module}&action={action}&{urlencode(api_params)}"
        res = requests.get(url).json()
        if res['status'] == '0' or res['message'] == 'NOTOK':
            raise Exception(res['result'])
        return res['result']
    
    def update_supported_chains(self):
        res = requests.get(CHAINLIST_URL).json()
        # check if the request is successful
        if res['status'] == '0' or res['message'] == 'NOTOK':
            raise Exception(res['result'])
        self._cached_supported_chains = res['result']
    
    def connect(self):
        """
        https://api.etherscan.io/v2/api
        ?chainid=1
        &module=gastracker
        &action=gasoracle
        &apikey=YourApiKeyToken 

        Raises:
            Exception: _description_
        """
        res = self.GasTracker.gasoracle()
        if res['status'] != '1' or res['message'] != 'OK':
            raise Exception(res['result'])
        print("EtherscanV2 API connect successfully.")
