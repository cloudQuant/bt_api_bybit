"""Module-level docstring."""

import pytest
from bt_api_base.containers.requestdatas.request_data import RequestData

from bt_api_bybit.feeds.request_base import BybitRequestData


def test_bybit_defaults_exchange_name() -> None:
    """test_bybit_defaults_exchange_name function"""
    request_data = BybitRequestData(public_key="public-key", private_key="secret-key")

    assert request_data.exchange_name == "BYBIT___SPOT"


def test_bybit_request_allows_missing_extra_data(monkeypatch) -> None:
    """test_bybit_request_allows_missing_extra_data function"""
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
    """test_bybit_accepts_api_key_and_api_secret_aliases function"""
    request_data = BybitRequestData(api_key="public-key", api_secret="secret-key")

    assert request_data.public_key == "public-key"
    assert request_data.private_key == "secret-key"


def test_bybit_error_response_raises_rate_limit() -> None:
    """API 错误(retCode != 0)必须翻译为 UnifiedError 并抛出。"""
    from bt_api_base.error import UnifiedError

    request_data = BybitRequestData(public_key="pk", private_key="sk")
    with pytest.raises(UnifiedError):
        request_data._raise_if_error({"retCode": 10006, "retMsg": "Rate limit exceeded"})


def test_bybit_error_response_raises_auth_error() -> None:
    from bt_api_base.error import UnifiedError

    request_data = BybitRequestData(public_key="pk", private_key="sk")
    with pytest.raises(UnifiedError):
        request_data._raise_if_error(
            {"retCode": 13001, "retMsg": "Signature verification failed"}
        )


def test_bybit_success_response_does_not_raise() -> None:
    """成功响应(retCode == 0)不抛异常。"""
    request_data = BybitRequestData(public_key="pk", private_key="sk")
    request_data._raise_if_error({"retCode": 0, "result": {}})
