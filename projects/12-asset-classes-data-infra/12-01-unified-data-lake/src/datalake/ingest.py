"""Backfill: pull candles from a source and upsert them into the store.

Idempotent by construction (the store upserts on the primary key), so re-running a backfill
over an overlapping window is safe — the basis for building long history going forward.
"""
from __future__ import annotations

from .sources.base import MarketData
from .store import DuckDBStore


def backfill(store: DuckDBStore, source: MarketData, instrument_key: str,
             interval: str = "1day", start=None, end=None) -> int:
    """Fetch from `source`, normalize (the source already does), upsert; return rows written."""
    df = source.candles(instrument_key, interval, start, end)
    return store.upsert_candles(df)
