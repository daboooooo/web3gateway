"""
Etherscan API Metadata Module

This module defines valid parameters and metadata for all API endpoints:
- Parameter validation maps
- Base URLs
- Endpoint definitions
"""

# Base API URL for all requests
base_url: str = "https://api.etherscan.io/v2/api"

# Valid parameters for each API action
# Format: 'action_name': ['param1', 'param2', ...]
valid_params = {
    # Account endpoints
    'balance': ['address', 'tag'],
    'balancemulti': ['address', 'tag'],
    'txlist': ['address', 'startblock', 'endblock', 'page', 'offset', 'sort'],
    'txlistinternal': ['address', 'txhash', 'startblock', 'endblock', 'page', 'offset', 'sort'],
    'tokentx': ['address', 'contractaddress', 'page', 'offset', 'startblock', 'endblock', 'sort'],
    'tokennfttx': ['address', 'contractaddress', 'page', 'offset', 'startblock',
                   'endblock', 'sort'],
    'token1155tx': ['address', 'contractaddress', 'page', 'offset', 'startblock',
                    'endblock', 'sort'],
    'getminedblocks': ['address', 'blocktype', 'page', 'offset'],
    'txsBeaconWithdrawal': ['address', 'contractaddress', 'page', 'offset',
                            'startblock', 'endblock', 'sort'],
    'balancehistory': ['address', 'blockno'],

    # Contracts
    'getabi': ['address'],
    'getsourcecode': ['address'],
    'getcontractcreation': ['contractaddresses'],
    'verifysourcecode': ['codeformat', 'sourceCode', 'constructorArguements', 'contractaddress',
                         'contractname',
                         'compilerversion'],
    'checkverifystatus': ['guid'],
    'verifyproxycontract': ['address'],
    'checkproxyverification': ['guid'],

    # Transactions
    'getstatus': ['txhash'],
    'gettxreceiptstatus': ['txhash'],

    # Block
    'getblockreward': ['blockno'],
    'getblockcountdown': ['blockno'],
    'getblocknobytime': ['timestamp', 'closest'],
    'dailyavgblocksize': ['startdate', 'enddate', 'sort'],
    'dailyblkcount': ['startdate', 'enddate', 'sort'],
    'dailyblockrewards': ['startdate', 'enddate', 'sort'],
    'dailyavgblocktime': ['startdate', 'enddate', 'sort'],
    'dailyuncleblkcount': ['startdate', 'enddate', 'sort'],

    # Logs
    'getLogs': ['address', 'fromBlock', 'toBlock', 'topic', 'topicOperator', 'page', 'offset'],

    # Geth/Parity Proxy
    'eth_blockNumber': [],
    'eth_getBlockByNumber': ['tag', 'boolean'],
    'eth_getUncleByBlockNumberAndIndex': ['tag', 'index'],
    'eth_getBlockTransactionCountByNumber': ['tag'],
    'eth_getTransactionByHash': ['txhash'],
    'eth_getTransactionByBlockNumberAndIndex': ['tag', 'index'],
    'eth_getTransactionCount': ['address', 'tag'],
    'eth_sendRawTransaction': ['hex'],
    'eth_getTransactionReceipt': ['txhash'],
    'eth_call': ['to', 'data', 'tag'],
    'eth_getCode': ['address', 'tag'],
    'eth_getStorageAt': ['address', 'position'],
    'eth_gasPrice': [],
    'eth_estimateGas': ['data', 'to', 'value', 'gas', 'gasPrice'],

    # Token
    'tokensupply': ['contractaddress'],
    'tokenbalance': ['contractaddress', 'address'],
    'tokensupplyhistory': ['contractaddress', 'blockno'],
    'tokenbalancehistory': ['contractaddress', 'address', 'blockno'],
    'tokenholderlist': ['contractaddress', 'page', 'offset'],
    'tokeninfo': ['contractaddress'],
    'addresstokenbalance': ['address', 'page', 'offset'],
    'addresstokennftbalance': ['address', 'page', 'offset'],
    'addresstokennftinventory': ['address', 'contractaddress', 'page', 'offset'],

    # Gas Tracker
    'gasestimate': ['gasprice'],
    'gasoracle': [],
    'dailyavggaslimit': ['startdate', 'enddate', 'sort'],
    'dailygasused': ['startdate', 'enddate', 'sort'],
    'dailyavggasprice': ['startdate', 'enddate', 'sort'],

    # Stats
    'ethsupply': [],
    'ethsupply2': [],
    'ethprice': [],
    'chainsize': ['startdate', 'enddate', 'clienttype', 'syncmode', 'sort'],
    'nodecount': [],
    'dailytxnfee': ['startdate', 'enddate', 'sort'],
    'dailynewaddress': ['startdate', 'enddate', 'sort'],
    'dailynetutilization': ['startdate', 'enddate', 'sort'],
    'dailyavghashrate': ['startdate', 'enddate', 'sort'],
    'dailytx': ['startdate', 'enddate', 'sort'],
    'dailyavgnetdifficulty': ['startdate', 'enddate', 'sort'],
    'ethdailymarketcap': ['startdate', 'enddate', 'sort'],
    'ethdailyprice': ['startdate', 'enddate', 'sort'],

    # Chain Specific
    'txnbridge': ['address', 'blocktype', 'page', 'offset'],

    # Usage
    'getapilimit': [],
}

# Parameter descriptions for documentation
param_descriptions = {
    "address": "Ethereum address (42 characters beginning with 0x)",
    "tag": "Pre-defined block parameter (earliest, pending, latest)",
    "startblock": "Starting block number for the query",
    "endblock": "Ending block number for the query",
    "page": "Page number for pagination",
    "offset": "Number of records per page",
    "sort": "Sorting preference (asc/desc)",
    "contractaddress": "Contract address",
    "txhash": "Transaction hash",
    "blockno": "Block number",
    "timestamp": "Unix timestamp",
    "closest": "Direction to find closest block (before/after)"
}
