"""
Chain Information Management Module

This module provides functionality to:
- Fetch and manage EVM-compatible blockchain network information
- Load and save chain configurations from/to JSON files
- Select and retrieve specific chain information
- Handle Infura project integration

The chain information structure follows the chainid.network format.
"""

import json
from typing import Any, Optional

import requests

from web3gateway.config import data_folder


class Chains:
    """
    Blockchain network information management class.

    This class handles the loading, saving, and selection of blockchain network
    configurations. It supports both local JSON files and remote updates from
    chainid.network.

    Attributes:
        infura_project_id (str): Infura project ID for RPC endpoints
        chains_json (Optional[dict]): Loaded chain configurations
        selected_chain (Optional[dict]): Currently selected chain info

    Example:
        chains = Chains("your-infura-project-id")
        chains.update_chains_json()
        chains.select_chain_by_key_value("chainId", 1)
        rpc_urls = chains.get_selected_chain_value("rpc")
    """

    def __init__(self, infura_project_id: str, chains_json: Optional[dict[str, Any]] = None):
        """
        Initialize Chains instance.

        Args:
            infura_project_id: Project ID for Infura RPC endpoints
            chains_json: Optional pre-loaded chain configurations
        """
        self.infura_project_id = infura_project_id

        if chains_json is None:
            self.update_chains_json()
        else:
            self.chains_json = chains_json

        self.selected_chain = None

    def update_chains_json(self):
        """
        Update chain information from chainid.network.

        Downloads the latest chain configurations and saves them locally.

        Raises:
            ConnectionError: If unable to fetch chain information
        """
        url = "https://chainid.network/chains.json"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            raise ConnectionError(f"Failed to get {url}")
        self.chains_json = response.json()
        self.save_chains_json()

    def save_chains_json(self) -> None:
        """
        Save chain configurations to local JSON file.

        Creates data directory if it doesn't exist and saves the current
        chain configurations to chains.json.
        """
        # Ensure data directory exists
        if not data_folder.exists():
            data_folder.mkdir()

        # Save configurations to JSON file
        with open(data_folder.joinpath("chains.json"), "w", encoding='utf-8') as f:
            json.dump(self.chains_json, f, indent=4)
        print("data/chains.json has been saved.")

    def load_chains_json_file(self) -> bool:
        """
        Load chain configurations from local JSON file.

        Returns:
            bool: True if successful, False if file not found
        """
        chain_file = data_folder.joinpath("chains.json")
        if not chain_file.exists():
            print(f"chains.json not found in {data_folder}")
            return False

        with open(chain_file, encoding='utf-8') as f:
            self.chains_json = json.load(f)
        print("data/chains.json has been loaded.")
        return True

    def select_chain_by_key_value(self, key: str, value: Any) -> bool:
        """
        Select a chain configuration by matching key and value.

        Args:
            key: Chain configuration key to match
            value: Value to match against

        Returns:
            bool: True if chain found and selected, False otherwise

        Raises:
            ValueError: If chains_json is not loaded
        """
        if self.chains_json is None:
            raise ValueError("chains_json is None")

        for chain_info in self.chains_json:
            if isinstance(chain_info, dict) and chain_info.get(key) == value:
                self.selected_chain = chain_info.copy()
                return True
        return False

    def get_selected_chain_value(self, key: str) -> Any:
        """
        Get a specific value from the selected chain configuration.

        Args:
            key: Configuration key to retrieve

        Returns:
            Any: Configuration value

        Raises:
            ValueError: If no chain is selected
            KeyError: If key doesn't exist in selected chain

        Note:
            Special handling for 'rpc' key to inject Infura project ID
        """
        if self.selected_chain is None:
            raise ValueError("selected_chain is None")

        if key not in self.selected_chain:
            raise KeyError(f"key {key} not found in selected_chain")

        # Special handling for RPC endpoints to inject Infura project ID
        if key == "rpc":
            return [rpc.replace(
                "${INFURA_API_KEY}",
                self.infura_project_id) for rpc in self.selected_chain[key]]

        return self.selected_chain.get(key)
