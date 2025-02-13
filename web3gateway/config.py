import json
from pathlib import Path
from typing import Any, Optional


project_path = Path().resolve()
source_folder = project_path.joinpath('web3gateway/')
data_folder = project_path.joinpath('data/')
log_folder = project_path.joinpath('logs/')
config_file = project_path.joinpath('config.json')
config_example_file = project_path.joinpath('config.json.example')


def load_config_json(my_config_file: Optional[Path]) -> dict[str, Any]:
    """ load environment variables from file and validate required variables """
    # check file existence
    if my_config_file:
        _config_file = my_config_file
    else:
        _config_file = config_file
    if not _config_file.exists():
        raise FileNotFoundError(f"Environment file not found: {_config_file}")

    # load config.json
    with open(_config_file, encoding='utf-8') as fo:
        config = json.load(fo)

    with open(config_example_file, encoding='utf-8') as fo:
        config_example = json.load(fo)

    missing_vars = [var for var in config_example if var not in config]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    return config
