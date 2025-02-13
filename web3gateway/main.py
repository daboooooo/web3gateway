import logging
from datetime import datetime
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from web3 import Web3

from web3gateway.config import load_config_json
from web3gateway.gateway_blockchain import Blockchain
from web3gateway.gateway_etherscanv2 import EtherScanV2


# gateway instances
config = load_config_json(None)
gw_etherscan = EtherScanV2(config)
gw_blockchain = Blockchain(config)

app = FastAPI(title="Web3 Restful API Gateway")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def with_timestamp(data: Dict[str, Any]) -> Dict[str, Any]:
    """为响应数据添加时间戳（毫秒级）"""
    return {
        "timestamp": int(datetime.utcnow().timestamp() * 1000),
        "data": data
    }


@app.get("/ping")
async def ping():
    return with_timestamp({"message": "pong"})


class AssembleTranactionRequest(BaseModel):
    chain_id: int
    tx_params: Dict[str, Any]
    gas_level: str


@app.post("/transaction/assemble")
async def assemble_tx(request: AssembleTranactionRequest):
    try:
        # convert address to checksum address
        from_address = Web3.to_checksum_address(request.tx_params['from'].lower())
        to_address = Web3.to_checksum_address(request.tx_params['to'].lower())
        # call blockchain gateway to assemble transaction
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
    chain_id: int
    raw_tx: str


@app.post("/transaction/send")
async def send_transaction(request: SendTransactionRequest):
    try:
        tx_hash = await gw_blockchain.send_raw_transaction(
            request.chain_id, request.raw_tx)
        return with_timestamp({"transaction_hash": tx_hash})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class GetTransactionReceiptRequest(BaseModel):
    chain_id: int
    tx_hash: str


@app.post("/transaction/get_receipt")
async def get_transaction_receipt(request: GetTransactionReceiptRequest):
    """ get transaction status """
    try:
        receipt = await gw_blockchain.get_transaction_receipt(
            request.chain_id, request.tx_hash)
        return with_timestamp({"status": receipt['status'] if receipt else None})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


class AccountBalanceRequest(BaseModel):
    chain_id: int
    address: str


@app.post("/account/balance")
async def get_account_balance(request: AccountBalanceRequest):
    try:
        gw_etherscan.set_chain_id(request.chain_id)
        address = Web3.to_checksum_address(request.address)
        balance = await gw_etherscan.account.balance(address)
        return with_timestamp({"balance": balance if balance is not None else "0"})
    except Exception as e:
        logging.exception(f"Error getting balance for {request.chain_id}:{request.address}")
        raise HTTPException(status_code=500, detail=str(e))


class AccountTokenBalanceRequest(BaseModel):
    chain_id: int
    contractaddress: str
    address: str


@app.post("/account/token_balance")
async def get_account_token_balance(request: AccountTokenBalanceRequest):
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
                               "token balance": response['result']})
    except Exception as e:
        logging.exception("Error getting tokens for "
                          f"{request.chain_id}:{request.contractaddress}:{request.address}")
        raise HTTPException(status_code=500, detail=str(e))


class AccountTransactionsRequest(BaseModel):
    chain_id: int
    address: str


@app.post("/account/txlist")
async def get_account_transactions(request: AccountTransactionsRequest):
    try:
        gw_etherscan.set_chain_id(request.chain_id)
        txs = await gw_etherscan.account.txlist(request.address)
        return with_timestamp({"last transactions": txs})
    except Exception as e:
        logging.exception(f"Error getting transactions for {request.chain_id}:{request.address}")
        raise HTTPException(status_code=500, detail=str(e))


# start uvicorn main:app --reload
def main():
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
