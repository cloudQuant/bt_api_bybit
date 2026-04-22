# Bybit Documentation

<!-- English -->
## English

Welcome to the **Bybit** documentation for bt_api.

**Bybit** is a cryptocurrency derivatives exchange offering Spot trading and USDT-Margined Perpetual Futures (Linear contracts). It is known for high liquidity and deep order books on major trading pairs.

### Overview

`bt_api_bybit` provides a unified interface to Bybit exchange through the bt_api plugin architecture. It supports:

- **Spot Trading**: Market data and order placement for spot pairs
- **Linear Futures**: USDT-margined perpetual futures trading
- **Market Data**: Ticker, Order Book, K-Lines, Trade History, Server Time
- **Account**: Balance queries, Order management

### Installation

```bash
pip install bt_api_bybit
```

### Quick Start

```python
from bt_api_py import BtApi

# Initialize without authentication (public data only)
api = BtApi()

# Spot ticker (public)
ticker = api.get_tick("BYBIT___SPOT", "BTCUSDT")
print(f"BTCUSDT spot: {ticker}")

# Linear futures ticker (public)
ticker_linear = api.get_tick("BYBIT___LINEAR", "BTCUSDT")
print(f"BTCUSDT linear: {ticker_linear}")

# With authentication
api_auth = BtApi(exchange_kwargs={
    "BYBIT___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    }
})

# Get balance
balance = api_auth.get_balance("BYBIT___SPOT")

# Place order
order = api_auth.make_order(
    exchange_name="BYBIT___SPOT",
    symbol="BTCUSDT",
    volume=0.001,
    price=67000,
    order_type="limit",
)
```

### Supported Operations

#### Spot (BYBIT___SPOT)

| Operation | Auth Required | Description |
|-----------|---------------|-------------|
| `get_tick` | No | 24hr rolling ticker |
| `get_depth` | No | Order book depth |
| `get_kline` | No | Candlestick data |
| `get_exchange_info` | No | Market listings |
| `get_server_time` | No | Server timestamp |
| `get_deals` | No | Trade execution records |
| `get_balance` | Yes | Asset balances |
| `get_account` | Yes | Account information |
| `make_order` | Yes | Place limit/market order |
| `cancel_order` | Yes | Cancel pending order |
| `query_order` | Yes | Query order by ID |

#### Linear Futures (BYBIT___LINEAR)

| Operation | Auth Required | Description |
|-----------|---------------|-------------|
| `get_tick` | No | 24hr rolling ticker |
| `get_depth` | No | Order book depth |
| `get_kline` | No | Candlestick data |
| `get_exchange_info` | No | Contract listings |
| `get_balance` | Yes | Account balances |
| `get_account` | Yes | Account information |
| `make_order` | Yes | Place limit/market order |
| `cancel_order` | Yes | Cancel pending order |
| `query_order` | Yes | Query order by ID |

### Supported Symbols

- **Spot**: `BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `XRPUSDT`, `BNBUSDT`, and 100+ more
- **Linear Futures**: `BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `BNBUSDT`, and 100+ perpetual futures

### Exchange Codes

```
BYBIT___SPOT     # Spot trading
BYBIT___LINEAR   # USDT-margined perpetual futures
```

### Error Handling

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BYBIT___SPOT": {
        "api_key": "invalid_key",
        "secret": "invalid_secret",
    }
})

try:
    balance = api.get_balance("BYBIT___SPOT")
except Exception as e:
    print(f"Error: {e}")
```

### Rate Limits

| Endpoint Type | Limit |
|---------------|-------|
| Public endpoints | 600 requests/minute |
| Private endpoints | 60 requests/minute |
| Order placement | 200 requests/minute |

### More Information

- [GitHub Repository](https://github.com/cloudQuant/bt_api_bybit)
- [Issue Tracker](https://github.com/cloudQuant/bt_api_bybit/issues)
- [bt_api Documentation](https://cloudquant.github.io/bt_api_py/)
- [bt_api_base Documentation](https://bt-api-base.readthedocs.io/)

---

## 中文

欢迎使用 bt_api 的 **Bybit** 文档。

**Bybit** 是一家加密货币衍生品交易所，提供现货交易和 USDT 保证金永续合约（线性合约）。它以主要交易对的高流动性和深度订单簿著称。

### 概述

`bt_api_bybit` 通过 bt_api 插件架构提供连接 Bybit 交易所的统一接口。支持：

- **现货交易**：现货交易对的市场数据和下单
- **线性合约**：USDT 保证金永续合约交易
- **行情数据**：行情、订单簿、K线、成交历史、服务器时间
- **账户**：余额查询、订单管理

### 安装

```bash
pip install bt_api_bybit
```

### 快速开始

```python
from bt_api_py import BtApi

# 初始化（无需认证，仅获取公开数据）
api = BtApi()

# 现货行情（公开接口）
ticker = api.get_tick("BYBIT___SPOT", "BTCUSDT")
print(f"BTCUSDT 现货: {ticker}")

# 线性合约行情（公开接口）
ticker_linear = api.get_tick("BYBIT___LINEAR", "BTCUSDT")
print(f"BTCUSDT 线性: {ticker_linear}")

# 需要认证的操作
api_auth = BtApi(exchange_kwargs={
    "BYBIT___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    }
})

# 获取余额
balance = api_auth.get_balance("BYBIT___SPOT")

# 下单
order = api_auth.make_order(
    exchange_name="BYBIT___SPOT",
    symbol="BTCUSDT",
    volume=0.001,
    price=67000,
    order_type="limit",
)
```

### 支持的操作

#### 现货 (BYBIT___SPOT)

| 操作 | 需要认证 | 说明 |
|------|---------|------|
| `get_tick` | 否 | 24小时滚动行情 |
| `get_depth` | 否 | 订单簿深度 |
| `get_kline` | 否 | K线数据 |
| `get_exchange_info` | 否 | 市场列表 |
| `get_server_time` | 否 | 服务器时间戳 |
| `get_deals` | 否 | 成交记录 |
| `get_balance` | 是 | 资产余额 |
| `get_account` | 是 | 账户信息 |
| `make_order` | 是 | 下限价/市价单 |
| `cancel_order` | 是 | 取消挂单 |
| `query_order` | 是 | 按ID查询订单 |

#### 线性合约 (BYBIT___LINEAR)

| 操作 | 需要认证 | 说明 |
|------|---------|------|
| `get_tick` | 否 | 24小时滚动行情 |
| `get_depth` | 否 | 订单簿深度 |
| `get_kline` | 否 | K线数据 |
| `get_exchange_info` | 否 | 合约列表 |
| `get_balance` | 是 | 账户余额 |
| `get_account` | 是 | 账户信息 |
| `make_order` | 是 | 下限价/市价单 |
| `cancel_order` | 是 | 取消挂单 |
| `query_order` | 是 | 按ID查询订单 |

### 支持的交易对

- **现货**: `BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `XRPUSDT`, `BNBUSDT` 等 100+ 交易对
- **线性合约**: `BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `BNBUSDT` 等 100+ 永续合约

### 交易所代码

```
BYBIT___SPOT     # 现货交易
BYBIT___LINEAR   # USDT保证金永续合约
```

### 错误处理

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BYBIT___SPOT": {
        "api_key": "invalid_key",
        "secret": "invalid_secret",
    }
})

try:
    balance = api.get_balance("BYBIT___SPOT")
except Exception as e:
    print(f"错误: {e}")
```

### 限流配置

| 端点类型 | 限制 |
|---------|------|
| 公开接口 | 600 次/分钟 |
| 私有接口 | 60 次/分钟 |
| 下单接口 | 200 次/分钟 |

### 更多信息

- [GitHub 仓库](https://github.com/cloudQuant/bt_api_bybit)
- [问题反馈](https://github.com/cloudQuant/bt_api_bybit/issues)
- [bt_api 文档](https://cloudquant.github.io/bt_api_py/)
- [bt_api_base 文档](https://bt-api-base.readthedocs.io/)
