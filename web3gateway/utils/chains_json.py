"""
{
        "name": "Ethereum Mainnet",
        "chain": "ETH",
        "icon": "ethereum",
        "rpc": [
            "https://mainnet.infura.io/v3/${INFURA_API_KEY}",
            "wss://mainnet.infura.io/ws/v3/${INFURA_API_KEY}",
            "https://api.mycryptoapi.com/eth",
            "https://cloudflare-eth.com",
            "https://ethereum-rpc.publicnode.com",
            "wss://ethereum-rpc.publicnode.com",
            "https://mainnet.gateway.tenderly.co",
            "wss://mainnet.gateway.tenderly.co",
            "https://rpc.blocknative.com/boost",
            "https://rpc.flashbots.net",
            "https://rpc.flashbots.net/fast",
            "https://rpc.mevblocker.io",
            "https://rpc.mevblocker.io/fast",
            "https://rpc.mevblocker.io/noreverts",
            "https://rpc.mevblocker.io/fullprivacy",
            "https://eth.drpc.org",
            "wss://eth.drpc.org"
        ],
        "features": [
            {
                "name": "EIP155"
            },
            {
                "name": "EIP1559"
            }
        ],
        "faucets": [],
        "nativeCurrency": {
            "name": "Ether",
            "symbol": "ETH",
            "decimals": 18
        },
        "infoURL": "https://ethereum.org",
        "shortName": "eth",
        "chainId": 1,
        "networkId": 1,
        "slip44": 60,
        "ens": {
            "registry": "0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e"
        },
        "explorers": [
            {
                "name": "etherscan",
                "url": "https://etherscan.io",
                "standard": "EIP3091"
            },
            {
                "name": "blockscout",
                "url": "https://eth.blockscout.com",
                "icon": "blockscout",
                "standard": "EIP3091"
            },
            {
                "name": "dexguru",
                "url": "https://ethereum.dex.guru",
                "icon": "dexguru",
                "standard": "EIP3091"
            }
        ]
    },
"""
import json
from typing import Any, Optional

import requests

from web3gateway.config import data_folder


class Chains:
    def __init__(self, infura_project_id: str, chains_json: Optional[dict[str, Any]] = None):
        self.infura_project_id = infura_project_id

        if chains_json is None:
            self.update_chains_json()
        else:
            self.chains_json = chains_json

        self.selected_chain = None

    def update_chains_json(self):
        """ update chains.json from chainid.network """
        url = "https://chainid.network/chains.json"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            raise ConnectionError(f"Failed to get {url}")
        self.chains_json = response.json()
        self.save_chains_json()

    def save_chains_json(self) -> None:
        """ save chains.json to local file """
        # check data_folder
        if not data_folder.exists():
            data_folder.mkdir()
        # save chains.json
        with open(data_folder.joinpath("chains.json"), "w", encoding='utf-8') as f:
            json.dump(self.chains_json, f, indent=4)
        print("data/chains.json has been saved.")

    def load_chains_json_file(self) -> bool:
        """ load chains.json from local file """
        # check data_folder/chains.json is exists
        if not data_folder.joinpath("chains.json").exists():
            print(f"chains.json not found in {data_folder}")
            return False
        with open(data_folder.joinpath("chains.json"), encoding='utf-8') as f:
            self.chains_json = json.load(f)
        print("data/chains.json has been loaded.")
        return True

    def select_chain_by_key_value(self, key: str, value: Any) -> bool:
        """ select a chain by key value """
        if self.chains_json is None:
            raise ValueError("chains_json is None")
        for chain_info in self.chains_json:
            if isinstance(chain_info, dict) and chain_info.get(key) == value:
                self.selected_chain = chain_info.copy()
                return True
        return False

    def get_selected_chain_value(self, key: str) -> Any:
        """ get value from selected_chain """
        if self.selected_chain is None:
            raise ValueError("selected_chain is None")
        if key not in self.selected_chain:
            raise KeyError(f"key {key} not found in selected_chain")
        if key == "rpc":
            return [rpc.replace("${INFURA_API_KEY}",
                                self.infura_project_id) for rpc in self.selected_chain[key]]
        return self.selected_chain.get(key)
