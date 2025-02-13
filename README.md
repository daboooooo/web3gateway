# Web3 Restful Gateway

## 项目简介

Web3 Restful Gateway 是多链支持的Web3网关服务，为区块链应用提供一个统一的Restful API接口，支持多条EVM兼容区块链的查询和交互功能。

## 核心功能

1. 多链地址查询
   - 账户余额查询
   - Token持仓查询
   - 交易历史查询

2. 多链交易服务
   - Gas费用评估
   - 交易发送
   - 交易状态追踪

3. 系统服务
   - 健康检查(Pingpong)
   - 链状态监控

## 技术特点

- 基于Web3.py和Infura实现区块链交互
- 集成Etherscan API V2实现多链数据查询，限流5次/秒
  - https://docs.etherscan.io/etherscan-v2
- 使用Redis实现查询结果缓存，，缓存有效期5秒
- 利用环境变量配置Etherscan API V2 密钥和Infura Project ID，以及Redis连接信息，免去rest api调用者的密钥管理

## 支持的功能

1. 多链支持
   - 从 https://api.etherscan.io/v2/chainlist 获取支持的链列表，通过ChainID进行链的选择和切换
   - 统一的API接口适配多条链

2. Gas管理
   - 实时Gas评估
   - 交易成本预测

3. 交易处理
   - 签名交易发送
   - 交易状态查询

4. 数据查询
   - 地址余额查询
   - Token余额查询
   - 交易历史记录
   - 缓存支持的快速查询


## 测试命令

以下是针对各个 RESTful API 的测试命令，使用地址 `0x32f7cb25353f1acae03ade9ca8e91ecad57fd7b0`：

1. **Ping API**

```bash
curl -X GET "http://localhost:8000/ping"
```

2. **Assemble Transaction API**

```bash
curl -X POST "http://localhost:8000/transaction/assemble" -H "Content-Type: application/json" -d '{
    "chain_id": 1,
    "tx_params": {
        "from": "0x32f7cb25353f1acae03ade9ca8e91ecad57fd7b0",
        "to": "0x32f7cb25353f1acae03ade9ca8e91ecad57fd7b0",
        "value": "0x0",
        "data": ""
    },
    "gas_level": "standard"
}'
```

3. **Send Transaction API**

```bash
curl -X POST "http://localhost:8000/transaction/send" -H "Content-Type: application/json" -d '{
    "chain_id": 1,
    "raw_tx": "0x..."
}'
```

4. **Get Transaction Receipt API**

```bash
curl -X POST "http://localhost:8000/transaction/get_receipt" -H "Content-Type: application/json" -d '{
    "chain_id": 1,
    "tx_hash": "0x..."
}'
```

5. **Get Account Balance API**

```bash
curl -X POST "http://localhost:8000/account/balance" -H "Content-Type: application/json" -d '{
    "chain_id": 1,
    "address": "0x32f7cb25353f1acae03ade9ca8e91ecad57fd7b0"
}'
```

6. **Get Account Token Balance API**

```bash
curl -X POST "http://localhost:8000/account/token_balance" -H "Content-Type: application/json" -d '{
    "chain_id": 1,
    "contractaddress": "0x...",
    "address": "0x32f7cb25353f1acae03ade9ca8e91ecad57fd7b0"
}'
```

7. **Get Account Transactions API**

```bash
curl -X POST "http://localhost:8000/account/txlist" -H "Content-Type: application/json" -d '{
    "chain_id": 1,
    "address": "0x32f7cb25353f1acae03ade9ca8e91ecad57fd7b0"
}'
```

请根据实际情况替换 `0x...` 部分的值。
