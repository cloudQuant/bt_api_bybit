"""Module documentation"""
from __future__ import annotations

import os
from typing import Any

from bt_api_base.containers.exchanges.exchange_data import ExchangeData
from bt_api_base.logging_factory import get_logger

logger = get_logger("bybit_exchange_data")

# ──  ──────────────────────────────────────────────
_bybit_config = None
_bybit_config_loaded = False


def _get_bybit_config() -> Any | None:
    """ Bybit YAML ."""
    global _bybit_config, _bybit_config_loaded
    if _bybit_config_loaded:
        return _bybit_config
    try:
        from bt_api_base.config_loader import load_exchange_config

        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "configs",
            "bybit.yaml",
        )
        if os.path.exists(config_path):
            _bybit_config = load_exchange_config(config_path)
        _bybit_config_loaded = True
    except (OSError, ValueError, KeyError, ImportError) as e:
        logger.warning(f"Failed to load bybit.yaml config: {e}")
    return _bybit_config


class BybitExchangeData(ExchangeData):
    """Base class for all Bybit exchange types.

    Provides shared utility methods (get_symbol, get_period, get_rest_path,
    get_wss_path, account_wss_symbol) and default kline_periods.
    Subclasses MUST set exchange-specific: exchange_name, rest_url,
    acct_wss_url, wss_url, rest_paths, wss_paths, legal_currency.
    """

    def __init__(self) -> None:
        """__init__ method"""
        super().__init__()
        self.exchange_name = "bybit"
        self.rest_url = ""
        self.acct_wss_url = ""
        self.wss_url = ""
        self.rest_paths: dict[str, str] = {}
        self.wss_paths: dict[str, str] = {}

        self.kline_periods = {
            "1s": "1",
            "1m": "1",
            "3m": "3",
            "5m": "5",
            "15m": "15",
            "30m": "30",
            "1h": "60",
            "2h": "120",
            "4h": "240",
            "6h": "360",
            "8h": "480",
            "12h": "720",
            "1d": "D",
            "3d": "3d",
            "1w": "W",
            "1M": "M",
        }
        self.reverse_kline_periods = {v: k for k, v in self.kline_periods.items()}

        self.legal_currency = [
            "USDT",
            "USD",
            "BTC",
            "ETH",
        ]

    def _load_from_config(self, asset_type) -> bool:
        """ YAML .

        Args: asset_type:  key,  'swap', 'spot', 'option'
        Returns: bool:

        """
        config = _get_bybit_config()
        if config is None:
            return False
        asset_cfg = config.asset_types.get(asset_type)
        if asset_cfg is None:
            return False

        # exchange_name
        if asset_cfg.exchange_name:
            self.exchange_name = asset_cfg.exchange_name

        # URLs ( base_urls ， asset_cfg)
        if config.base_urls:
            self.rest_url = config.base_urls.rest.get(asset_type, self.rest_url)
            self.wss_url = config.base_urls.wss.get(asset_type, self.wss_url)
            self.acct_wss_url = config.base_urls.acct_wss.get(asset_type, self.acct_wss_url)

        # rest_paths (, )
        if asset_cfg.rest_paths:
            self.rest_paths = dict(asset_cfg.rest_paths)

        # wss_paths: YAML  → {'params': [template], 'method': 'SUBSCRIBE', 'id': 1}
        if asset_cfg.wss_paths:
            converted = {}
            for key, value in asset_cfg.wss_paths.items():
                if isinstance(value, str):
                    if value:
                        converted[key] = {"params": [value], "method": "SUBSCRIBE", "id": 1}
                    else:
                        converted[key] = ""
                else:
                    converted[key] = value
            self.wss_paths = converted

        # kline_periods (asset-level ,  exchange-level)
        kp = asset_cfg.kline_periods or (config.kline_periods if config.kline_periods else None)
        if kp:
            self.kline_periods = dict(kp)
            self.reverse_kline_periods = {v: k for k, v in self.kline_periods.items()}

        # legal_currency (asset-level ,  exchange-level)
        lc = asset_cfg.legal_currency or (config.legal_currency if config.legal_currency else None)
        if lc:
            self.legal_currency = list(lc)

        return True

    def get_symbol(self, symbol: str) -> str:
        """ Bybit API （）."""
        return symbol.upper()

    def get_symbol_path(self, symbol):
        """， REST API."""
        return symbol.upper()

    def get_period(self, period: str) -> str:
        """ Bybit API ."""
        period = period.lower()
        return self.kline_periods.get(period, period)

    def get_period_path(self, period):
        """， REST API."""
        period = period.lower()
        return self.kline_periods.get(period, period)

    def get_rest_path(self, path_name: str, **kwargs) -> str:
        """ REST API ."""
        return self.rest_paths.get(path_name, "")

    def get_wss_path(self, module, symbol: str | None = None, **kwargs) -> str:
        """ WebSocket ."""
        return self.wss_paths.get(module, "")

    def account_wss_symbol(self, symbol: str) -> str:
        """ WebSocket ."""
        return symbol

    def get_default_period(self) -> str:
        """."""
        return "1m"

    def get_max_limit(self, module):
        """."""
        limits = {
            "tickers": 100,
            "depth": 200,
            "klines": 1000,
            "trades": 500,
        }
        return limits.get(module, 100)

    def get_reverse_period(self, api_period: str) -> str:
        """ API ."""
        return self.reverse_kline_periods.get(api_period, api_period)


class BybitExchangeDataSpot(BybitExchangeData):
    """Bybit ."""

    def __init__(self) -> None:
        """__init__ method"""
        super().__init__()
        self.asset_type = "spot"
        self._load_from_config(self.asset_type)


class BybitExchangeDataSwap(BybitExchangeData):
    """Bybit ."""

    def __init__(self) -> None:
        """__init__ method"""
        super().__init__()
        self.asset_type = "swap"
        self._load_from_config(self.asset_type)
