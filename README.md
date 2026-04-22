# bt_api_bybit

[![PyPI Version](https://img.shields.io/pypi/v/bt_api_bybit.svg)](https://pypi.org/project/bt_api_bybit/)
[![Python Versions](https://img.shields.io/pypi/pyversions/bt_api_bybit.svg)](https://pypi.org/project/bt_api_bybit/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/cloudQuant/bt_api_bybit/actions/workflows/ci.yml/badge.svg)](https://github.com/cloudQuant/bt_api_bybit/actions)
[![Docs](https://readthedocs.org/projects/bt-api-bybit/badge/?version=latest)](https://bt-api-bybit.readthedocs.io/)

---

<!-- English -->
# bt_api_bybit

> **Bybit exchange plugin for bt_api** — Unified REST API for **Spot** and **Linear (USDT-M) Futures** trading.

`bt_api_bybit` is a runtime plugin for [bt_api](https://github.com/cloudQuant/bt_api_py) that connects to **Bybit** exchange. It depends on [bt_api_base](https://github.com/cloudQuant/bt_api_base) for core infrastructure.

| Resource | Link |
|----------|------|
| English Docs | https://bt-api-bybit.readthedocs.io/ |
| Chinese Docs | https://bt-api-bybit.readthedocs.io/zh/latest/ |
| GitHub | https://github.com/cloudQuant/bt_api_bybit |
| PyPI | https://pypi.org/project/bt_api_bybit/ |
| Issues | https://github.com/cloudQuant/bt_api_bybit/issues |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| Main Project | https://github.com/cloudQuant/bt_api_py |

---

## Features

### 2 Asset Types

| Asset Type | Code | REST | Description |
|---|---|---|---|
| Spot | `BYBIT___SPOT` | ✅ | Spot trading |
| Linear Futures | `BYBIT___LINEAR` | ✅ | USDT-margined perpetual futures |

### Supported Operations

| Category | Operation | Spot | Linear |
|---|---|---|---|
| **Market Data** | `get_tick` / `get_ticker` | ✅ | ✅ |
| | `get_depth` | ✅ | ✅ |
| | `get_kline` | ✅ | ✅ |
| | `get_exchange_info` | ✅ | ✅ |
| | `get_server_time` | ✅ | ✅ |
| | `get_deals` | ✅ | ✅ |
| **Account** | `get_balance` | ✅ | ✅ |
| | `get_account` | ✅ | ✅ |
| **Trading** | `make_order` | ✅ | ✅ |
| | `cancel_order` | ✅ | ✅ |
| | `query_order` | ✅ | ✅ |

### Plugin Architecture

Auto-registers at import time via `ExchangeRegistry`. Works seamlessly with `BtApi`:

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BYBIT___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    },
    "BYBIT___LINEAR": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    },
})

# Spot market data (public - no auth required)
ticker = api.get_tick("BYBIT___SPOT", "BTCUSDT")

# Linear futures ticker
ticker_swap = api.get_tick("BYBIT___LINEAR", "BTCUSDT")

# Account balance (requires auth)
balance = api.get_balance("BYBIT___SPOT")

# Place order (requires auth)
order = api.make_order(
    exchange_name="BYBIT___SPOT",
    symbol="BTCUSDT",
    volume=0.001,
    price=67000,
    order_type="limit",
)
```

---

## Installation

### From PyPI (Recommended)

```bash
pip install bt_api_bybit
```

### From Source

```bash
git clone https://github.com/cloudQuant/bt_api_bybit
cd bt_api_bybit
pip install -e .
```

### Requirements

- Python `3.9` – `3.14`
- `bt_api_base >= 0.15`

---

## Quick Start

### 1. Install

```bash
pip install bt_api_bybit
```

### 2. Get ticker (public — no API key needed)

```python
from bt_api_py import BtApi

api = BtApi()
ticker = api.get_tick("BYBIT___SPOT", "BTCUSDT")
print(f"BTCUSDT spot price: {ticker}")
```

### 3. Place an order (requires API key)

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BYBIT___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    }
})

order = api.make_order(
    exchange_name="BYBIT___SPOT",
    symbol="BTCUSDT",
    volume=0.001,
    price=67000,
    order_type="limit",
)
print(f"Order placed: {order}")
```

### 4. Linear Futures

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BYBIT___LINEAR": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    }
})

# Get linear futures ticker
ticker = api.get_tick("BYBIT___LINEAR", "BTCUSDT")

# Place linear futures order
order = api.make_order(
    exchange_name="BYBIT___LINEAR",
    symbol="BTCUSDT",
    volume=0.001,
    price=67000,
    order_type="limit",
)
```

---

## Architecture

```
bt_api_bybit/
├── plugin.py                     # register_plugin() — bt_api plugin entry point
├── registry_registration.py      # register_bybit() — feeds / exchange_data registration
├── exchange_data/
│   └── bybit_exchange_data.py  # BybitExchangeData base + Spot/Swap subclasses
├── feeds/
│   ├── request_base.py        # BybitRequestData — REST base class
│   ├── spot.py               # BybitRequestDataSpot — spot operations
│   └── swap.py               # BybitRequestDataSwap — linear futures operations
├── containers/
│   ├── tickers/              # Ticker containers
│   ├── orderbooks/           # OrderBook containers
│   ├── orders/              # Order containers
│   └── balances/             # Balance containers
└── errors/
    └── bybit_translator.py  # BybitErrorTranslator → bt_api_base.ApiError
```

---

## Supported Symbols

- **Spot**: `BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `XRPUSDT`, and 100+ more trading pairs
- **Linear Futures**: `BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `BNBUSDT`, and 100+ perpetual futures

---

## Error Handling

All Bybit API errors are translated to bt_api_base `ApiError` subclasses:

| Bybit Code | Error | Description |
|---|---|---|
| `0` | Success | No error |
| `10001` | `PARAM_ERROR` | Missing or invalid parameter |
| `10003` | `PARAM_ERROR` | Invalid request format |
| `10004` | `REQUEST_ERROR` | Invalid request path |
| `10005` | `RESPONSE_ERROR` | Invalid response format |
| `10006` | `RATE_LIMIT` | Rate limit exceeded |
| `10010` | `ACCOUNT_ERROR` | Account error |
| `10012` | `BALANCE_ERROR` | Insufficient balance |
| `10014` | `SYMBOL_ERROR` | Symbol not found |
| `10016` | `ORDER_NOT_FOUND` | Order not found |
| `10017` | `ORDER_ERROR` | Invalid order price or quantity |
| `10020` | `MARKET_ERROR` | Market closed |
| `10029` | `ORDER_ERROR` | Duplicate order |
| `11001` | `LEVERAGE_ERROR` | Invalid leverage |
| `11003` | `MARGIN_ERROR` | Insufficient margin |
| `13000` | `API_KEY_ERROR` | API key error |
| `13001` | `AUTH_ERROR` | Signature verification failed |
| `13002` | `AUTH_ERROR` | Invalid IP address |
| `13003` | `AUTH_ERROR` | Missing API key |
| `13004` | `AUTH_ERROR` | Invalid timestamp |
| `13005` | `AUTH_ERROR` | Permission denied |

---

## Rate Limits

| Endpoint | Limit |
|---|---|
| Public endpoints | 600 requests/minute |
| Private endpoints | 60 requests/minute |
| Order placement | 200 requests/minute |

---

## Documentation

| Doc | Link |
|-----|------|
| **English** | https://bt-api-bybit.readthedocs.io/ |
| **中文** | https://bt-api-bybit.readthedocs.io/zh/latest/ |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| Main Project | https://cloudquant.github.io/bt_api_py/ |

---

## License

MIT — see [LICENSE](LICENSE).

---

## Support

- [GitHub Issues](https://github.com/cloudQuant/bt_api_bybit/issues) — bug reports, feature requests
- Email: yunjinqi@gmail.com

---

---

## 中文

> **bt_api 的 Bybit 交易所插件** — 为**现货**和** USDT 永续合约**交易提供统一的 REST API。

`bt_api_bybit` 是 [bt_api](https://github.com/cloudQuant/bt_api_py) 的运行时插件，连接 **Bybit** 交易所。依赖 [bt_api_base](https://github.com/cloudQuant/bt_api_base) 提供核心基础设施。

| 资源 | 链接 |
|------|------|
| 英文文档 | https://bt-api-bybit.readthedocs.io/ |
| 中文文档 | https://bt-api-bybit.readthedocs.io/zh/latest/ |
| GitHub | https://github.com/cloudQuant/bt_api_bybit |
| PyPI | https://pypi.org/project/bt_api_bybit/ |
| 问题反馈 | https://github.com/cloudQuant/bt_api_bybit/issues |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| 主项目 | https://github.com/cloudQuant/bt_api_py |

---

## 功能特点

### 2 种资产类型

| 资产类型 | 代码 | REST | 说明 |
|---|---|---|---|
| 现货 | `BYBIT___SPOT` | ✅ | 现货交易 |
| 线性合约 | `BYBIT___LINEAR` | ✅ | USDT 保证金永续合约 |

### 支持的操作

| 类别 | 操作 | 现货 | 线性合约 |
|---|---|---|---|
| **行情数据** | `get_tick` / `get_ticker` | ✅ | ✅ |
| | `get_depth` | ✅ | ✅ |
| | `get_kline` | ✅ | ✅ |
| | `get_exchange_info` | ✅ | ✅ |
| | `get_server_time` | ✅ | ✅ |
| | `get_deals` | ✅ | ✅ |
| **账户** | `get_balance` | ✅ | ✅ |
| | `get_account` | ✅ | ✅ |
| **交易** | `make_order` | ✅ | ✅ |
| | `cancel_order` | ✅ | ✅ |
| | `query_order` | ✅ | ✅ |

### 插件架构

通过 `ExchangeRegistry` 在导入时自动注册，与 `BtApi` 无缝协作：

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BYBIT___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    },
    "BYBIT___LINEAR": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    },
})

# 现货行情（公开接口，无需认证）
ticker = api.get_tick("BYBIT___SPOT", "BTCUSDT")

# 线性合约行情
ticker_swap = api.get_tick("BYBIT___LINEAR", "BTCUSDT")

# 账户余额（需要认证）
balance = api.get_balance("BYBIT___SPOT")

# 下单（需要认证）
order = api.make_order(
    exchange_name="BYBIT___SPOT",
    symbol="BTCUSDT",
    volume=0.001,
    price=67000,
    order_type="limit",
)
```

---

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install bt_api_bybit
```

### 从源码安装

```bash
git clone https://github.com/cloudQuant/bt_api_bybit
cd bt_api_bybit
pip install -e .
```

### 系统要求

- Python `3.9` – `3.14`
- `bt_api_base >= 0.15`

---

## 快速开始

### 1. 安装

```bash
pip install bt_api_bybit
```

### 2. 获取行情（公开接口，无需 API key）

```python
from bt_api_py import BtApi

api = BtApi()
ticker = api.get_tick("BYBIT___SPOT", "BTCUSDT")
print(f"BTCUSDT 现货价格: {ticker}")
```

### 3. 下单交易（需要 API key）

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BYBIT___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    }
})

order = api.make_order(
    exchange_name="BYBIT___SPOT",
    symbol="BTCUSDT",
    volume=0.001,
    price=67000,
    order_type="limit",
)
print(f"订单已下单: {order}")
```

### 4. 线性合约

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BYBIT___LINEAR": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    }
})

# 获取线性合约行情
ticker = api.get_tick("BYBIT___LINEAR", "BTCUSDT")

# 下线性合约订单
order = api.make_order(
    exchange_name="BYBIT___LINEAR",
    symbol="BTCUSDT",
    volume=0.001,
    price=67000,
    order_type="limit",
)
```

---

## 架构

```
bt_api_bybit/
├── plugin.py                     # register_plugin() — bt_api 插件入口点
├── registry_registration.py      # register_bybit() — feeds / exchange_data 注册
├── exchange_data/
│   └── bybit_exchange_data.py  # BybitExchangeData 基类 + Spot/Swap 子类
├── feeds/
│   ├── request_base.py        # BybitRequestData — REST 基类
│   ├── spot.py               # BybitRequestDataSpot — 现货操作
│   └── swap.py               # BybitRequestDataSwap — 线性合约操作
├── containers/
│   ├── tickers/              # 行情容器
│   ├── orderbooks/           # 订单簿容器
│   ├── orders/               # 订单容器
│   └── balances/             # 余额容器
└── errors/
    └── bybit_translator.py  # BybitErrorTranslator → bt_api_base.ApiError
```

---

## 支持的交易对

- **现货**: `BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `XRPUSDT` 等 100+ 交易对
- **线性合约**: `BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `BNBUSDT` 等 100+ 永续合约

---

## 错误处理

所有 Bybit API 错误均翻译为 bt_api_base `ApiError` 子类：

| Bybit 错误码 | 错误类型 | 说明 |
|---|---|---|
| `0` | 成功 | 无错误 |
| `10001` | `PARAM_ERROR` | 缺少或无效参数 |
| `10003` | `PARAM_ERROR` | 无效请求格式 |
| `10004` | `REQUEST_ERROR` | 无效请求路径 |
| `10005` | `RESPONSE_ERROR` | 无效响应格式 |
| `10006` | `RATE_LIMIT` | 请求过于频繁 |
| `10010` | `ACCOUNT_ERROR` | 账户错误 |
| `10012` | `BALANCE_ERROR` | 余额不足 |
| `10014` | `SYMBOL_ERROR` | 交易对未找到 |
| `10016` | `ORDER_NOT_FOUND` | 订单未找到 |
| `10017` | `ORDER_ERROR` | 无效订单价格或数量 |
| `10020` | `MARKET_ERROR` | 市场已关闭 |
| `10029` | `ORDER_ERROR` | 重复订单 |
| `11001` | `LEVERAGE_ERROR` | 无效杠杆 |
| `11003` | `MARGIN_ERROR` | 保证金不足 |
| `13000` | `API_KEY_ERROR` | API key 错误 |
| `13001` | `AUTH_ERROR` | 签名验证失败 |
| `13002` | `AUTH_ERROR` | IP 地址无效 |
| `13003` | `AUTH_ERROR` | 缺少 API key |
| `13004` | `AUTH_ERROR` | 无效时间戳 |
| `13005` | `AUTH_ERROR` | 权限不足 |

---

## 限流配置

| 端点 | 限制 |
|---|---|
| 公开接口 | 600 次/分钟 |
| 私有接口 | 60 次/分钟 |
| 下单接口 | 200 次/分钟 |

---

## 文档

| 文档 | 链接 |
|-----|------|
| **英文文档** | https://bt-api-bybit.readthedocs.io/ |
| **中文文档** | https://bt-api-bybit.readthedocs.io/zh/latest/ |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| 主项目 | https://cloudquant.github.io/bt_api_py/ |

---

## 许可证

MIT — 详见 [LICENSE](LICENSE)。

---

## 技术支持

- [GitHub Issues](https://github.com/cloudQuant/bt_api_bybit/issues) — bug 报告、功能请求
- 邮箱: yunjinqi@gmail.com
