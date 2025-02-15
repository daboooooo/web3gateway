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
   - 健康检查(Ping-Pong)
   - 链状态监控

## 技术特点

- 基于Web3.py和Infura实现区块链交互
- 集成Etherscan API V2实现多链数据查询，限流5次/秒
  - https://docs.etherscan.io/etherscan-v2
- 使用Redis实现查询结果缓存

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
