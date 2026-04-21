from unittest.mock import AsyncMock
import pytest
from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_bybit.feeds.request_base import BybitRequestData


def test_bybit_defaults_exchange_name() -> None:
    request_data = BybitRequestData(public_key="public-key", private_key="secret-key")

    assert request_data.exchange_name == "BYBIT___SPOT"


def test_bybit_request_allows_missing_extra_data(monkeypatch) -> None:
    request_data = BybitRequestData(
        public_key="public-key",
        private_key="secret-key",
        exchange_name="BYBIT___SPOT",
    )

    monkeypatch.setattr(
        request_data,
        "http_request",
        lambda method, url, headers, body, timeout: {"retCode": 0, "result": {}},
    )

    result = request_data.request("GET /v5/market/time")

    assert isinstance(result, RequestData)
    assert result.get_extra_data() == {}
    assert result.get_input_data() == {"retCode": 0, "result": {}}


def test_bybit_accepts_api_key_and_api_secret_aliases() -> None:
    request_data = BybitRequestData(api_key="public-key", api_secret="secret-key")

    assert request_data.public_key == "public-key"
    assert request_data.private_key == "secret-key"
