"""Module documentation"""
from __future__ import annotations

import time
from typing import Any

from bt_api_base.containers.balances.balance import BalanceData
from bt_api_base.logging_factory import get_logger

logger = get_logger("container")


class BybitBalanceData(BalanceData):
    """ Bybit """

    def __init__(
        self,
        balance_info: dict[str, Any],
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        """Bybit。

        Args: balance_info: 。
            asset_type: （ spot、swap ）。
            has_been_json_encoded:  JSON ， False。
        """
        super().__init__(balance_info, has_been_json_encoded)
        self.exchange_name = "BYBIT"
        self.local_update_time = time.time()
        self.asset_type = asset_type
        self.balance_data = balance_info if has_been_json_encoded else None
        self.account_type: str | None = None
        self.total_equity: float | None = None
        self.total_wallet_balance: float | None = None
        self.total_available_balance: float | None = None
        self.coins: list[dict[str, Any]] = []
        self.all_data: dict[str, Any] | None = None
        self.has_been_init_data = False

    def init_data(self) -> BybitBalanceData:
        """。

        Returns: BybitBalanceData 。
        """
        if self.has_been_init_data or self.balance_data is None:
            return self

        try:
            result = self.balance_data.get("result", {})
            list_data = result.get("list", [])

            if not list_data:
                return self

            account = list_data[0]  # Bybit ，

            #
            self.account_type = account.get("accountType")
            self.total_equity = account.get("totalEquity")
            self.total_wallet_balance = account.get("totalWalletBalance")
            self.total_available_balance = account.get("totalAvailableBalance")

            #
            coins_data = account.get("coin", [])
            self.coins = []

            for coin_info in coins_data:
                coin = {
                    "coin": coin_info.get("coin"),
                    "wallet_balance": float(coin_info.get("walletBalance", 0)),
                    "available_to_withdraw": float(coin_info.get("availableToWithdraw", 0)),
                    "locked": float(coin_info.get("locked", 0)),
                    "equity": float(coin_info.get("equity", 0)),
                    "unrealised_pnl": float(coin_info.get("unrealisedPnl", 0)),
                }
                self.coins.append(coin)

            self.has_been_init_data = True

        except Exception as e:
            logger.error(f"Error parsing Bybit balance data: {e}", exc_info=True)

            self.has_been_init_data = False
        return self

    def get_all_data(self) -> dict[str, Any]:
        """。

        Returns: 。
        """
        if self.all_data is None:
            self.init_data()
            self.all_data = {
                "exchange_name": self.exchange_name,
                "asset_type": self.asset_type,
                "local_update_time": self.local_update_time,
                "account_type": self.account_type,
                "total_equity": self.total_equity,
                "total_wallet_balance": self.total_wallet_balance,
                "total_available_balance": self.total_available_balance,
                "coins": self.coins,
            }
        return self.all_data

    def get_coin_balance(self, coin: str) -> dict[str, Any] | None:
        """。

        Args: coin: 。

        Returns: ， None。
        """
        for coin_info in self.coins:
            if coin_info["coin"] == coin.upper():
                return coin_info
        return None

    def get_available_balance(self, coin: str) -> float:
        """。

        Args: coin: 。

        Returns: 。
        """
        coin_info = self.get_coin_balance(coin)
        if coin_info:
            return coin_info["available_to_withdraw"]
        return 0.0

    def get_locked_balance(self, coin: str) -> float:
        """。

        Args: coin: 。

        Returns: 。
        """
        coin_info = self.get_coin_balance(coin)
        if coin_info:
            return coin_info["locked"]
        return 0.0

    def get_total_balance(self, coin: str) -> float:
        """。

        Args: coin: 。

        Returns: 。
        """
        coin_info = self.get_coin_balance(coin)
        if coin_info:
            return coin_info["wallet_balance"]
        return 0.0

    def get_unrealised_pnl(self, coin: str) -> float:
        """。

        Args: coin: 。

        Returns: 。
        """
        coin_info = self.get_coin_balance(coin)
        if coin_info:
            return coin_info["unrealised_pnl"]
        return 0.0

    def get_all_available_balances(self) -> dict[str, float]:
        """。

        Returns: ，，。
        """
        return {coin["coin"]: coin["available_to_withdraw"] for coin in self.coins}

    def get_total_equity(self) -> float:
        """。

        Returns: 。
        """
        return float(self.total_equity) if self.total_equity else 0.0

    def get_total_wallet_balance(self) -> float:
        """。

        Returns: 。
        """
        return float(self.total_wallet_balance) if self.total_wallet_balance else 0.0

    def has_balance(self, coin: str) -> bool:
        """。

        Args: coin: 。

        Returns: True， False。
        """
        return self.get_available_balance(coin) > 0

    def __str__(self) -> str:
        """。

        Returns: 。
        """
        self.init_data()
        return (
            f"BybitBalance(account_type={self.account_type}, "
            f"total_equity={self.total_equity}, "
            f"available={self.total_available_balance})"
        )

    def get_exchange_name(self) -> str:
        """。

        Returns: "BYBIT"。
        """
        return self.exchange_name

    def get_asset_type(self) -> str:
        """。

        Returns: 。
        """
        return self.asset_type

    def get_server_time(self) -> float:
        """。

        Returns: 。
        """
        return self.local_update_time

    def get_local_update_time(self) -> float:
        """。

        Returns: 。
        """
        return self.local_update_time

    def get_account_id(self) -> str | None:
        """ID。

        Returns: ID。
        """
        return self.account_type

    def get_account_type(self) -> str | None:
        """。

        Returns: 。
        """
        return self.account_type

    def get_fee_tier(self) -> str | None:
        """。

        Returns: （）。
        """
        return None

    def get_max_withdraw_amount(self) -> float | None:
        """。

        Returns: （）。
        """
        return None

    def get_margin(self) -> float | None:
        """。

        Returns: （）。
        """
        return None

    def get_used_margin(self) -> float | None:
        """。

        Returns: （）。
        """
        return None

    def get_maintain_margin(self) -> float | None:
        """。

        Returns: （）。
        """
        return None

    def get_available_margin(self) -> float | None:
        """。

        Returns: （）。
        """
        return None

    def get_open_order_initial_margin(self) -> float | None:
        """。

        Returns: （）。
        """
        return None

    def get_position_initial_margin(self) -> float | None:
        """。

        Returns: （）。
        """
        return None

    def get_unrealized_profit(self) -> float | None:
        """。

        Returns: （）。
        """
        return None

    def get_interest(self) -> float | None:
        """。

        Returns: （）。
        """
        return None


class BybitSpotBalanceData(BybitBalanceData):
    """Bybit """

    def __init__(self, balance_info: dict[str, Any], has_been_json_encoded: bool = False) -> None:
        """Bybit。

        Args: balance_info: 。
            has_been_json_encoded:  JSON ， False。
        """
        super().__init__(balance_info, "spot", has_been_json_encoded)

    def init_data(self) -> BybitSpotBalanceData:
        """。

        Returns: BybitSpotBalanceData 。
        """
        return super().init_data()  # type: ignore


class BybitSwapBalanceData(BybitBalanceData):
    """Bybit /swap """

    def __init__(self, balance_info: dict[str, Any], has_been_json_encoded: bool = False) -> None:
        """Bybit。

        Args: balance_info: 。
            has_been_json_encoded:  JSON ， False。
        """
        super().__init__(balance_info, "swap", has_been_json_encoded)

    def init_data(self) -> BybitSwapBalanceData:
        """。

        Returns: BybitSwapBalanceData 。
        """
        return super().init_data()  # type: ignore
