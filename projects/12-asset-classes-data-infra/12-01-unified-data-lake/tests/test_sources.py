"""Offline tests for the source layer — no network, no token.

The yfinance raw->canonical mapping is pure, so we feed it a synthetic yfinance-shaped
frame; the live fetch itself is exercised by the opt-in smoke script, not here.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from datalake import COLUMNS, DuckDBStore, backfill, normalize  # noqa: E402
from datalake.sources import YFinanceSource, available  # noqa: E402


def _yahoo_frame(n=3):
    idx = pd.DatetimeIndex(pd.date_range("2026-08-25", periods=n, freq="D"), name="Date")
    return pd.DataFrame({"Open": 1.0, "High": 2.0, "Low": 0.5, "Close": 1.5,
                         "Adj Close": 1.5, "Volume": 100}, index=idx)


def test_yfinance_mapper_matches_schema():
    out = YFinanceSource._to_candles(_yahoo_frame(3), "^NSEI", "1day")
    assert list(out.columns) == COLUMNS
    assert len(out) == 3
    assert (out["source"] == "yfinance").all()
    assert out["instrument_key"].iloc[0] == "^NSEI"
    assert out["ts"].iloc[0].utcoffset() == pd.Timedelta(hours=5, minutes=30)


def test_yfinance_mapper_empty():
    out = YFinanceSource._to_candles(pd.DataFrame(), "X", "1day")
    assert list(out.columns) == COLUMNS and len(out) == 0


def test_backfill_writes_to_store():
    class FakeSource:
        name = "fake"

        def candles(self, key, interval="1day", start=None, end=None):
            raw = pd.DataFrame({"ts": pd.date_range("2026-08-25", periods=2, freq="D"),
                                "open": 1, "high": 1, "low": 1, "close": 1, "volume": 1})
            return normalize(raw, key, interval, "fake")

    store = DuckDBStore()
    assert backfill(store, FakeSource(), "K", "1day") == 2
    assert store.count() == 2
    store.close()


def test_yfinance_registered():
    assert "yfinance" in available()
