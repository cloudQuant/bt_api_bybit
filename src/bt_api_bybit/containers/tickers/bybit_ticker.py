"""Module documentation"""
from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from bt_api_base._compat import Self

from bt_api_base.containers.tickers.ticker import TickerData
from bt_api_base.functions.utils import from_dict_get_float
from bt_api_base.logging_factory import get_logger

logger = get_logger("container")


class BybitTickerData(TickerData):
    """ Bybit ticker ."""

    def __init__(self, ticker_info, symbol_name, asset_type, has_been_json_encoded=False) -> None:
        """__init__ method"""
        super().__init__(ticker_info, has_been_json_encoded)
        self.exchange_name = "BYBIT"  # 
        self.local_update_time = time.time()  # 
        self.symbol_name = symbol_name
        self.asset_type = asset_type  # ticker
        self.ticker_data: dict[str, Any] | None = ticker_info if has_been_json_encoded else None
        self.ticker_symbol_name: str | None = None
        self.server_time: float | None = None
        self.bid_price: float | None = None
        self.ask_price: float | None = None
        self.bid_volume: float | None = None
        self.ask_volume: float | None = None
        self.last_price: float | None = None
        self.last_volume: float | None = None
        self.high_price_24h: float | None = None
        self.low_price_24h: float | None = None
        self.volume_24h: float | None = None
        self.turnover_24h: float | None = None
        self.price_change_24h: float | None = None
        self.price_change_percent_24h: float | None = None
        self.all_data: dict[str, Any] | None = None
        self.has_been_init_data = False

    def init_data(self) -> Self:
        """ ticker ."""
        if self.has_been_init_data or self.ticker_data is None:
            return self

        try:
            result = (self.ticker_data or {}).get("result", {})
            list_data = result.get("list", [])

            if not list_data:
                return self

            ticker = list_data[0]  # Bybit ，

            # 
            self.ticker_symbol_name = ticker.get("symbol")
            self.server_time = ticker.get("time", 0)

            # 
            self.last_price = from_dict_get_float(ticker, "lastPrice")
            self.bid_price = from_dict_get_float(ticker, "bid1Price")
            self.ask_price = from_dict_get_float(ticker, "ask1Price")

            # 
            self.bid_volume = from_dict_get_float(ticker, "bid1Size")
            self.ask_volume = from_dict_get_float(ticker, "ask1Size")
            self.last_volume = from_dict_get_float(ticker, "volume24h")

            # 24
            self.high_price_24h = from_dict_get_float(ticker, "highPrice24h")
            self.low_price_24h = from_dict_get_float(ticker, "lowPrice24h")
            self.volume_24h = from_dict_get_float(ticker, "volume24h")
            self.turnover_24h = from_dict_get_float(ticker, "turnover24h")

            # 
            prev_price_24h = from_dict_get_float(ticker, "prevPrice24h")
            if prev_price_24h and self.last_price:
                self.price_change_24h = self.last_price - prev_price_24h
                self.price_change_percent_24h = (self.price_change_24h / prev_price_24h) * 100

            self.has_been_init_data = True

        except Exception as e:
            logger.error(f"Error parsing Bybit ticker data: {e}", exc_info=True)

            self.has_been_init_data = False
        return self

    def get_all_data(self) -> dict[str, Any]:
        """ ticker ."""
        if self.all_data is None:
            self.init_data()
            self.all_data = {
                "exchange_name": self.exchange_name,
                "symbol_name": self.symbol_name,
                "asset_type": self.asset_type,
                "local_update_time": self.local_update_time,
                "ticker_symbol_name": self.ticker_symbol_name,
                "server_time": self.server_time,
                "last_price": self.last_price,
                "bid_price": self.bid_price,
                "ask_price": self.ask_price,
                "bid_volume": self.bid_volume,
                "ask_volume": self.ask_volume,
                "last_volume": self.last_volume,
                "high_price_24h": self.high_price_24h,
                "low_price_24h": self.low_price_24h,
                "volume_24h": self.volume_24h,
                "turnover_24h": self.turnover_24h,
                "price_change_24h": self.price_change_24h,
                "price_change_percent_24h": self.price_change_percent_24h,
            }
        return self.all_data or {}

    def __str__(self) -> str:
        """ ticker ."""
        self.init_data()
        return (
            f"BybitTicker(symbol={self.symbol_name}, "
            f"last={self.last_price}, "
            f"bid={self.bid_price}, "
            f"ask={self.ask_price}, "
            f"volume={self.volume_24h})"
        )


class BybitSpotTickerData(BybitTickerData):
    """Bybit  ticker ."""

    def __init__(self, ticker_info, symbol_name, has_been_json_encoded=False) -> None:
        """__init__ method"""
        super().__init__(ticker_info, symbol_name, "spot", has_been_json_encoded)


class BybitSwapTickerData(BybitTickerData):
    """Bybit /swap ticker ."""

    def __init__(self, ticker_info, symbol_name, has_been_json_encoded=False) -> None:
        """__init__ method"""
        super().__init__(ticker_info, symbol_name, "swap", has_been_json_encoded)
