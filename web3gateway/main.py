from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

import logging

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from config.chains import ChainId
from services.blockchain import BlockchainService
from services.cache import CacheService
from config.settings import settings
from adapters.explorer import ExplorerAPIException
import asyncio


app = FastAPI(title="Web3 Rest Gateway")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 服务实例
blockchain_service = BlockchainService()
cache_service = CacheService(redis_url=settings.redis_url)


@app.on_event("startup")
async def startup_event():
    # 重新初始化链配置
    from config.chains import init_chain_configs
    init_chain_configs()
    # 初始化缓存服务
    await cache_service.initialize()


@app.on_event("shutdown")
async def shutdown_event():
    # 清理资源
    for adapter in getattr(app.state, 'explorer_adapters', {}).values():
        await adapter.close()


class TransactionRequest(BaseModel):
    model_config = {
        "arbitrary_types_allowed": True
    }

    chain_id: ChainId
    raw_transaction: str


def with_timestamp(data: Dict[str, Any]) -> Dict[str, Any]:
    """为响应数据添加时间戳（毫秒级）"""
    return {
        "timestamp": int(datetime.utcnow().timestamp() * 1000),
        "data": data
    }


@app.get("/ping")
async def ping():
    return with_timestamp({"message": "pong"})


@app.post("/transaction/estimate-gas")
async def estimate_gas(chain_id: ChainId, tx_params: dict):
    try:
        gas = await blockchain_service.estimate_gas(chain_id, tx_params)
        return with_timestamp({"estimated_gas": gas})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/transaction/send")
async def send_transaction(request: TransactionRequest):
    try:
        tx_hash = await blockchain_service.send_raw_transaction(
            request.chain_id, 
            request.raw_transaction
        )
        return with_timestamp({"transaction_hash": tx_hash})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/transaction/{chain_id}/{tx_hash}")
async def get_transaction_status(chain_id: ChainId, tx_hash: str):
    try:
        receipt = await blockchain_service.get_transaction_receipt(chain_id, tx_hash)
        return with_timestamp({"status": receipt['status'] if receipt else None})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 添加依赖注入函数
async def get_cache_service():
    return cache_service


@app.get("/account/{chain_id}/{address}/balance")
async def get_account_balance(
    chain_id: ChainId,
    address: str,
    cache: CacheService = Depends(get_cache_service)
):
    try:
        cache_key = f"balance:{chain_id}:{address}"
        if cached := await cache.get(cache_key):
            return with_timestamp({"balance": cached})

        balance = await blockchain_service.get_balance(chain_id, address)
        if balance is not None:
            await cache.set(cache_key, balance, expire=300)
        return with_timestamp({"balance": balance if balance is not None else "0"})
    except ExplorerAPIException as e:
        logging.error(f"Explorer API error for {chain_id}:{address}: {e.message} (code: {e.code})")
        if e.code == 'NO_DATA':
            return with_timestamp({"balance": "0"})
        raise HTTPException(status_code=503, detail=f"Explorer API error: {e.message}")
    except Exception as e:
        logging.exception(f"Error getting balance for {chain_id}:{address}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/account/{chain_id}/{address}/tokens")
async def get_account_tokens(
    chain_id: ChainId, 
    address: str,
    cache: CacheService = Depends(get_cache_service)
):
    try:
        cache_key = f"tokens:{chain_id}:{address}"
        if cached := await cache.get(cache_key):
            return with_timestamp({"tokens": cached})

        tokens = await blockchain_service.get_tokens(chain_id, address)
        await cache.set(cache_key, tokens, expire=300)
        return with_timestamp({"tokens": tokens})
    except ExplorerAPIException as e:
        logging.error(f"Explorer API error for {chain_id}:{address}: {e.message} (code: {e.code})")
        if e.code == 'NO_DATA':
            return with_timestamp({"tokens": []})
        raise HTTPException(status_code=503, detail=f"Explorer API error: {e.message}")
    except Exception as e:
        logging.exception(f"Error getting tokens for {chain_id}:{address}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/account/{chain_id}/{address}/transactions")
async def get_account_transactions(
    chain_id: ChainId, 
    address: str,
    cache: CacheService = Depends(get_cache_service)
):
    try:
        cache_key = f"transactions:{chain_id}:{address}"
        if cached := await cache.get(cache_key):
            return with_timestamp({"transactions": cached})

        txs = await blockchain_service.get_transactions(chain_id, address)
        await cache.set(cache_key, txs, expire=300)
        return with_timestamp({"transactions": txs})
    except ExplorerAPIException as e:
        logging.error(f"Explorer API error for {chain_id}:{address}: {e.message} (code: {e.code})")
        if e.code == 'NO_DATA':
            return with_timestamp({"transactions": []})
        raise HTTPException(status_code=503, detail=f"Explorer API error: {e.message}")
    except Exception as e:
        logging.exception(f"Error getting transactions for {chain_id}:{address}")
        raise HTTPException(status_code=500, detail=str(e))


# start uvicorn main:app --reload
def main():
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
