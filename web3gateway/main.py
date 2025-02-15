"""
Web3 RESTful Gateway Main Application

This module implements a FastAPI-based gateway service that provides:
- Multi-chain support for EVM compatible blockchains
- Account balance and transaction queries
- Transaction assembly and submission
- Basic authentication and CORS support
"""

import logging
from datetime import datetime
from typing import Any, Dict

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from web3 import Web3

from web3gateway.config import load_config_json
from web3gateway.gateway_blockchain import Blockchain
from web3gateway.gateway_etherscanv2 import EtherScanV2


# Initialize gateway instances with configuration
config = load_config_json(None)
gw_etherscan = EtherScanV2(config)  # Etherscan API gateway for blockchain queries
gw_blockchain = Blockchain(config)   # Direct blockchain interaction gateway

app = FastAPI(title="Web3 Restful API Gateway")

# Enable CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBasic()  # Basic HTTP authentication handler


def with_timestamp(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add millisecond-precision timestamp to response data

    Args:
        data (Dict[str, Any]): Response data to be wrapped

    Returns:
        Dict[str, Any]: Data wrapped with current timestamp
    """
    return {
        "timestamp": int(datetime.now().timestamp() * 1000),
        "data": data
    }


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Verify HTTP basic authentication credentials

    Args:
        credentials: HTTP basic auth credentials

    Raises:
        HTTPException: If authentication fails
    """
    username = config['auth_username']
    password = config['auth_password']
    if credentials.username != username or credentials.password != password:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.get("/ping")
async def ping():
    """Health check endpoint"""
    return with_timestamp({"message": "pong"})


class AssembleTranactionRequest(BaseModel):
    """
    Transaction assembly request schema

    Attributes:
        chain_id (int): Target blockchain network ID
        tx_params (Dict[str, Any]): Transaction parameters
        gas_level (str): Desired gas price level (slow/normal/fast)
    """
    chain_id: int
    tx_params: Dict[str, Any]
    gas_level: str


@app.post("/transaction/assemble")
async def assemble_tx(request: AssembleTranactionRequest,
                      credentials: HTTPBasicCredentials = Depends(authenticate)):
    """
    Assemble an unsigned transaction with proper gas settings

    Args:
        request: Transaction assembly parameters
        credentials: Auth credentials

    Returns:
        Dict: Assembled transaction data

    Raises:
        HTTPException: If assembly fails
    """
    try:
        # Convert addresses to checksum format for consistency
        from_address = Web3.to_checksum_address(request.tx_params['from'].lower())
        to_address = Web3.to_checksum_address(request.tx_params['to'].lower())
        # Call blockchain gateway to assemble transaction
        tx = await gw_blockchain.assemble_unsigned_transaction(
            request.chain_id,
            from_address,
            to_address,
            request.tx_params['value'],
            request.tx_params.get('data', ''),
            request.gas_level)
        return with_timestamp(tx)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class SendTransactionRequest(BaseModel):
    """
    Send transaction request schema

    Attributes:
        chain_id (int): Target blockchain network ID
        raw_tx (str): Raw transaction data
    """
    chain_id: int
    raw_tx: str


@app.post("/transaction/send")
async def send_transaction(request: SendTransactionRequest,
                           credentials: HTTPBasicCredentials = Depends(authenticate)):
    """
    Send a raw transaction to the blockchain

    Args:
        request: Send transaction parameters
        credentials: Auth credentials

    Returns:
        Dict: Transaction hash

    Raises:
        HTTPException: If sending fails
    """
    try:
        tx_hash = await gw_blockchain.send_raw_transaction(
            request.chain_id, request.raw_tx)
        return with_timestamp({"transaction_hash": tx_hash})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class GetTransactionReceiptRequest(BaseModel):
    """
    Get transaction receipt request schema

    Attributes:
        chain_id (int): Target blockchain network ID
        tx_hash (str): Transaction hash
    """
    chain_id: int
    tx_hash: str


@app.post("/transaction/get_receipt")
async def get_transaction_receipt(request: GetTransactionReceiptRequest,
                                  credentials: HTTPBasicCredentials = Depends(authenticate)):
    """
    Get the receipt of a transaction

    Args:
        request: Get receipt parameters
        credentials: Auth credentials

    Returns:
        Dict: Transaction receipt status

    Raises:
        HTTPException: If retrieval fails
    """
    try:
        receipt = await gw_blockchain.get_transaction_receipt(
            request.chain_id, request.tx_hash)
        return with_timestamp({"status": receipt['status'] if receipt else None})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class AccountBalanceRequest(BaseModel):
    """
    Account balance request schema

    Attributes:
        chain_id (int): Target blockchain network ID
        address (str): Account address
    """
    chain_id: int
    address: str


@app.post("/account/balance")
async def get_account_balance(request: AccountBalanceRequest,
                              credentials: HTTPBasicCredentials = Depends(authenticate)):
    """
    Get the balance of an account

    Args:
        request: Account balance parameters
        credentials: Auth credentials

    Returns:
        Dict: Account balance

    Raises:
        HTTPException: If retrieval fails
    """
    try:
        gw_etherscan.set_chain_id(request.chain_id)
        address = Web3.to_checksum_address(request.address)
        balance = await gw_etherscan.account.balance(address)
        return with_timestamp({"balance": balance if balance is not None else "0"})
    except Exception as e:
        logging.exception(f"Error getting balance for {request.chain_id}:{request.address}")
        raise HTTPException(status_code=500, detail=str(e))


class AccountTokenBalanceRequest(BaseModel):
    """
    Account token balance request schema

    Attributes:
        chain_id (int): Target blockchain network ID
        contractaddress (str): Token contract address
        address (str): Account address
    """
    chain_id: int
    contractaddress: str
    address: str


@app.post("/account/token_balance")
async def get_account_token_balance(request: AccountTokenBalanceRequest,
                                    credentials: HTTPBasicCredentials = Depends(authenticate)):
    """
    Get the token balance of an account

    Args:
        request: Token balance parameters
        credentials: Auth credentials

    Returns:
        Dict: Token balance

    Raises:
        HTTPException: If retrieval fails
    """
    try:
        gw_etherscan.set_chain_id(request.chain_id)
        contract_address = Web3.to_checksum_address(request.contractaddress)
        address = Web3.to_checksum_address(request.address)
        response = await gw_etherscan.tokens.tokenbalance(
            contract_address, address)
        # {
        #    "status":"1",
        #    "message":"OK",
        #    "result":"135499"  # token's smallest decimal representation.
        # }
        return with_timestamp({"contract address": contract_address,
                               "address": address,
                               "token balance": response})
    except Exception as e:
        logging.exception("Error getting tokens for "
                          f"{request.chain_id}:{request.contractaddress}:{request.address}")
        raise HTTPException(status_code=500, detail=str(e))


class AccountTransactionsRequest(BaseModel):
    """
    Account transactions request schema

    Attributes:
        chain_id (int): Target blockchain network ID
        address (str): Account address
    """
    chain_id: int
    address: str


@app.post("/account/txlist")
async def get_account_transactions(request: AccountTransactionsRequest,
                                   credentials: HTTPBasicCredentials = Depends(authenticate)):
    """
    Get the list of transactions for an account

    Args:
        request: Account transactions parameters
        credentials: Auth credentials

    Returns:
        Dict: List of transactions

    Raises:
        HTTPException: If retrieval fails
    """
    try:
        gw_etherscan.set_chain_id(request.chain_id)
        txs = await gw_etherscan.account.txlist(request.address)
        return with_timestamp({"last transactions": txs})
    except Exception as e:
        logging.exception(f"Error getting transactions for {request.chain_id}:{request.address}")
        raise HTTPException(status_code=500, detail=str(e))


def main():
    """
    Application entry point - starts the FastAPI server
    Using uvicorn with hot reload for development
    """
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
