"""The `MarketData` source protocol + a tiny registry.

Sources are swappable behind one interface so downstream code never cares whether a candle
came from Upstox (live, token), NSE bhavcopy (free EOD) or yfinance (free). Every source
returns frames already in the canonical schema (see `schema.normalize`).
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable

import pandas as pd


@runtime_checkable
class MarketData(Protocol):
    name: str

    def candles(self, instrument_key: str, interval: str = "1day",
                start=None, end=None) -> pd.DataFrame:
        """Normalized OHLCV(+oi) candles for one instrument/interval."""
        ...


_REGISTRY: dict[str, "MarketData"] = {}


def register(source: "MarketData") -> "MarketData":
    _REGISTRY[source.name] = source
    return source


def get(name: str) -> "MarketData":
    return _REGISTRY[name]


def available() -> list[str]:
    return sorted(_REGISTRY)
