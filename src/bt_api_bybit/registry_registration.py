from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bt_api_base.registry import ExchangeRegistry

from bt_api_bybit.exchange_data.bybit_exchange_data import (
    BybitExchangeDataSpot,
    BybitExchangeDataSwap,
)
from bt_api_bybit.feeds.spot import BybitRequestDataSpot
from bt_api_bybit.feeds.swap import BybitRequestDataSwap


def register_bybit(registry: type[ExchangeRegistry]) -> None:
    registry.register_feed("BYBIT___SPOT", BybitRequestDataSpot)
    registry.register_exchange_data("BYBIT___SPOT", BybitExchangeDataSpot)

    registry.register_feed("BYBIT___SWAP", BybitRequestDataSwap)
    registry.register_exchange_data("BYBIT___SWAP", BybitExchangeDataSwap)
