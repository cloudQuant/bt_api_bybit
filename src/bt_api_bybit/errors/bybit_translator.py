"""
Bybit API
"""

from __future__ import annotations

from bt_api_base.error import ErrorTranslator, UnifiedError, UnifiedErrorCode


class BybitErrorTranslator(ErrorTranslator):
    """Bybit API

    Bybit API :
    {
      "retCode": 10003,
      "retMsg": "Invalid API key",
      "retExtInfo": {},
      "time": 1672304484978
    }
    """

    ERROR_MAP = {
        10001: (UnifiedErrorCode.INVALID_PARAMETER, "Parameter error"),
        10003: (UnifiedErrorCode.INVALID_API_KEY, "Invalid API key"),
        10004: (UnifiedErrorCode.INVALID_SIGNATURE, "Invalid signature"),
        10005: (UnifiedErrorCode.PERMISSION_DENIED, "Permission denied"),
        10006: (UnifiedErrorCode.RATE_LIMIT_EXCEEDED, "Too many requests"),
        10016: (UnifiedErrorCode.INTERNAL_ERROR, "Server error"),
        110001: (UnifiedErrorCode.ORDER_NOT_FOUND, "Order does not exist"),
        110004: (UnifiedErrorCode.INSUFFICIENT_BALANCE, "Insufficient balance"),
        110007: (UnifiedErrorCode.INVALID_PRICE, "Order price is out of range"),
        110043: (UnifiedErrorCode.PERMISSION_DENIED, "Set margin mode first"),
    }

    @classmethod
    def translate(cls, raw_error: dict, venue: str) -> UnifiedError | None:
        """Bybit API ， retCode """
        ret_code = raw_error.get("retCode")
        ret_msg = raw_error.get("retMsg", "")

        if ret_code is not None:
            # ERROR_MAP 的键是整型；Bybit 的 retCode 在 JSON 里也是数字。
            # 历史实现写成 `str(ret_code) in cls.ERROR_MAP`（str 查 int 键），
            # 恒为 False —— 映射形同死代码。这里按整型查，并容忍字符串数字。
            try:
                code_key: object = int(ret_code)
            except (TypeError, ValueError):
                code_key = ret_code
            if code_key in cls.ERROR_MAP:
                unified_code, default_msg = cls.ERROR_MAP[code_key]
                if unified_code is None:
                    return None
                return UnifiedError(
                    code=unified_code,
                    category=cls._get_category(unified_code),
                    venue=venue,
                    message=ret_msg or default_msg,
                    original_error=f"{ret_code}: {ret_msg}",
                    context={"raw_response": raw_error},
                )

        return super().translate(raw_error, venue)
