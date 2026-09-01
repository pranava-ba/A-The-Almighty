"""Normalized market-data schema + DuckDB DDL for the unified data lake.

Every source (Upstox / NSE bhavcopy / yfinance) is coerced to ONE schema, so downstream
code never cares where a candle came from. Keyed by (instrument_key, interval, ts) for
idempotent, survivorship-safe backfill. All timestamps are tz-aware IST.
"""
from __future__ import annotations

import pandas as pd

COLUMNS = ["instrument_key", "interval", "ts",
           "open", "high", "low", "close", "volume", "oi", "source"]

DDL = """
CREATE TABLE IF NOT EXISTS candles (
    instrument_key VARCHAR     NOT NULL,
    interval       VARCHAR     NOT NULL,
    ts             TIMESTAMPTZ NOT NULL,
    open   DOUBLE,
    high   DOUBLE,
    low    DOUBLE,
    close  DOUBLE,
    volume BIGINT,
    oi     BIGINT,
    source VARCHAR,
    PRIMARY KEY (instrument_key, interval, ts)
);
"""

IST = "Asia/Kolkata"


def canonical(df: pd.DataFrame, source: str) -> pd.DataFrame:
    """Coerce a frame that ALREADY carries per-row `instrument_key`, `interval`, `ts` and
    o/h/l/c/volume (optional `oi`) to the canonical schema — tz-aware IST, nullable ints.
    Use this when one frame spans many instruments (e.g. a full NSE bhavcopy)."""
    n = len(df)
    out = pd.DataFrame(index=range(n))
    out["instrument_key"] = df["instrument_key"].to_numpy()
    out["interval"] = df["interval"].to_numpy()
    ts = pd.to_datetime(df["ts"])
    ts = ts.dt.tz_localize(IST) if ts.dt.tz is None else ts.dt.tz_convert(IST)
    out["ts"] = ts.to_numpy()
    for c in ("open", "high", "low", "close"):
        out[c] = pd.to_numeric(df[c], errors="coerce").to_numpy()
    out["volume"] = pd.array(pd.to_numeric(df.get("volume"), errors="coerce"), dtype="Int64")
    out["oi"] = (pd.array(pd.to_numeric(df["oi"], errors="coerce"), dtype="Int64")
                 if "oi" in df.columns else pd.array([pd.NA] * n, dtype="Int64"))
    out["source"] = source
    return out[COLUMNS]


def normalize(df: pd.DataFrame, instrument_key: str, interval: str, source: str) -> pd.DataFrame:
    """Single-instrument convenience wrapper over `canonical`: the source frame needs
    ts/open/high/low/close/volume (optional oi); key & interval are supplied here."""
    tmp = df.copy()
    tmp["instrument_key"] = instrument_key
    tmp["interval"] = interval
    return canonical(tmp, source)
