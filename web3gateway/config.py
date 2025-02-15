"""
Configuration Management Module

This module handles the loading and validation of configuration settings
from JSON files. It provides path management for project resources and
ensures all required configuration parameters are present.
"""

import json
from pathlib import Path
from typing import Any, Optional


# Define project directory structure
project_path = Path().resolve()  # Root project directory
source_folder = project_path.joinpath('web3gateway/')  # Source code directory
data_folder = project_path.joinpath('data/')  # Data storage directory
log_folder = project_path.joinpath('logs/')  # Logging directory
config_file = project_path.joinpath('config.json')  # Main configuration file
config_example_file = project_path.joinpath('config.json.example')  # Template configuration


def load_config_json(my_config_file: Optional[Path]) -> dict[str, Any]:
    """
    Load and validate configuration settings from a JSON file.

    This function reads configuration settings from a JSON file and validates
    them against a template to ensure all required settings are present.

    Args:
        my_config_file (Optional[Path]): Custom configuration file path.
            If None, uses the default config.json in project root.

    Returns:
        dict[str, Any]: Dictionary containing configuration settings

    Raises:
        FileNotFoundError: If configuration file does not exist
        ValueError: If required configuration variables are missing
        json.JSONDecodeError: If configuration file is not valid JSON

    Example:
        >>> config = load_config_json(None)
        >>> print(config['auth_username'])
        'admin'
    """
    # Use provided config file or fall back to default
    if my_config_file:
        _config_file = my_config_file
    else:
        _config_file = config_file

    # Verify config file exists
    if not _config_file.exists():
        raise FileNotFoundError(f"Environment file not found: {_config_file}")

    # Load actual configuration
    with open(_config_file, encoding='utf-8') as fo:
        config = json.load(fo)

    # Load template configuration for validation
    with open(config_example_file, encoding='utf-8') as fo:
        config_example = json.load(fo)

    # Validate all required variables are present
    missing_vars = [var for var in config_example if var not in config]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    return config
