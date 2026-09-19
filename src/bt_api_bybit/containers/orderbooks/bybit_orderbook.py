"""Module documentation"""
from __future__ import annotations

import time
from typing import Any

from bt_api_base.containers.orderbooks.orderbook import OrderBookData
from bt_api_base.logging_factory import get_logger

logger = get_logger("container")


class BybitOrderBookData(OrderBookData):
    """Bybit.

    Bybit，、，
    。
    """

    def __init__(
        self,
        orderbook_info: str | dict,
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        """Bybit.

        Args: orderbook_info: （JSON）
            symbol_name:
            asset_type: （ "SPOT", "SWAP"）
            has_been_json_encoded: JSON
        """
        super().__init__(orderbook_info, has_been_json_encoded)
        self.exchange_name = "BYBIT"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.orderbook_data: Any = orderbook_info if has_been_json_encoded else None
        self.bids: list[list[float]] = []
        self.asks: list[list[float]] = []
        self.timestamp: float | None = None
        self.update_id: int | None = None
        self.all_data: dict[str, Any] | None = None
        self.has_been_init_data = False

    def init_data(self) -> BybitOrderBookData:
        """.

        。

        Returns: BybitOrderBookData: self
        """
        if self.has_been_init_data or self.orderbook_data is None:
            return self

        try:
            result = self.orderbook_data.get("result", {})

            self.timestamp = result.get("ts")
            self.update_id = result.get("u")

            bids_data = result.get("b", [])
            asks_data = result.get("a", [])

            self.bids = []
            for bid in bids_data:
                if len(bid) >= 2:
                    price = float(bid[0])
                    quantity = float(bid[1])
                    self.bids.append([price, quantity])

            self.asks = []
            for ask in asks_data:
                if len(ask) >= 2:
                    price = float(ask[0])
                    quantity = float(ask[1])
                    self.asks.append([price, quantity])

            self.bids.sort(key=lambda x: x[0], reverse=True)
            self.asks.sort(key=lambda x: x[0])

            self.has_been_init_data = True

        except Exception as e:
            logger.error(f"Error parsing Bybit orderbook data: {e}", exc_info=True)

            self.has_been_init_data = False
        return self

    def get_all_data(self) -> dict[str, Any]:
        """.

        Returns: dict: 、、
        """
        if self.all_data is None:
            self.init_data()
            self.all_data = {
                "exchange_name": self.exchange_name,
                "symbol_name": self.symbol_name,
                "asset_type": self.asset_type,
                "local_update_time": self.local_update_time,
                "timestamp": self.timestamp,
                "update_id": self.update_id,
                "bids": self.bids,
                "asks": self.asks,
            }
        return self.all_data

    def get_best_bid(self) -> float | None:
        """.

        Returns: float | None: ，None
        """
        if self.bids:
            return self.bids[0][0]
        return None

    def get_best_ask(self) -> float | None:
        """.

        Returns: float | None: ，None
        """
        if self.asks:
            return self.asks[0][0]
        return None

    def get_spread(self) -> float | None:
        """.

        Returns: float | None: （ - ），None
        """
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()
        if best_bid is not None and best_ask is not None:
            return best_ask - best_bid
        return None

    def get_bid_depth(self, depth: int = 5) -> list[list[float]]:
        """.

        Args: depth: ，5

        Returns: list: （）
        """
        return self.bids[:depth]

    def get_ask_depth(self, depth: int = 5) -> list[list[float]]:
        """.

        Args: depth: ，5

        Returns: list: （）
        """
        return self.asks[:depth]

    def get_total_bid_qty(self) -> float:
        """.

        Returns: float:
        """
        return sum(bid[1] for bid in self.bids)

    def get_total_ask_qty(self) -> float:
        """.

        Returns: float:
        """
        return sum(ask[1] for ask in self.asks)

    def is_valid(self) -> bool:
        """.

        Returns: bool: True，False
        """
        return len(self.bids) > 0 and len(self.asks) > 0

    def __str__(self) -> str:
        """."""
        self.init_data()
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()
        return (
            f"BybitOrderBook(symbol={self.symbol_name}, "
            f"bid={best_bid}, "
            f"ask={best_ask}, "
            f"spread={self.get_spread()})"
        )


class BybitSpotOrderBookData(BybitOrderBookData):
    """Bybit."""

    def __init__(
        self,
        orderbook_info: str | dict,
        symbol_name: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        """Bybit.

        Args: orderbook_info: （JSON）
            symbol_name:
            has_been_json_encoded: JSON
        """
        super().__init__(orderbook_info, symbol_name, "spot", has_been_json_encoded)


class BybitSwapOrderBookData(BybitOrderBookData):
    """Bybit/swap."""

    def __init__(
        self,
        orderbook_info: str | dict,
        symbol_name: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        """Bybit.

        Args: orderbook_info: （JSON）
            symbol_name:
            has_been_json_encoded: JSON
        """
        super().__init__(orderbook_info, symbol_name, "swap", has_been_json_encoded)
