"""Offline tests for the data lake — synthetic fixtures, no network, no token."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from datalake import DuckDBStore, normalize  # noqa: E402


def _synthetic(n=5):
    ts = pd.date_range("2026-08-27 09:15", periods=n, freq="1min", tz="Asia/Kolkata")
    return pd.DataFrame({"ts": ts, "open": 100.0, "high": 101.0,
                         "low": 99.0, "close": 100.5, "volume": 1000})


def test_upsert_is_idempotent():
    store = DuckDBStore()
    df = normalize(_synthetic(), "NSE_INDEX|Nifty 50", "1minute", "synthetic")
    assert store.upsert_candles(df) == 5
    store.upsert_candles(df)                 # re-pull the same window
    assert store.count() == 5                # no duplicates
    out = store.read_candles("NSE_INDEX|Nifty 50", "1minute")
    assert len(out) == 5
    assert list(out.columns)[:3] == ["instrument_key", "interval", "ts"]
    store.close()


def test_upsert_updates_on_conflict():
    store = DuckDBStore()
    store.upsert_candles(normalize(_synthetic(1), "X", "1minute", "a"))
    df2 = normalize(_synthetic(1), "X", "1minute", "b")
    df2.loc[0, "close"] = 999.0
    store.upsert_candles(df2)
    out = store.read_candles("X", "1minute")
    assert out.loc[0, "close"] == 999.0
    assert out.loc[0, "source"] == "b"
    store.close()


def test_naive_ts_is_localized_to_ist():
    store = DuckDBStore()
    naive = pd.DataFrame({"ts": ["2026-08-27 09:15"], "open": 1, "high": 1, "low": 1,
                          "close": 1, "volume": 0})
    store.upsert_candles(normalize(naive, "Y", "1day", "s"))
    out = store.read_candles("Y", "1day")
    # IST is +5:30 regardless of the zone-name alias (DuckDB reports Asia/Calcutta)
    assert out.loc[0, "ts"].utcoffset() == pd.Timedelta(hours=5, minutes=30)
    store.close()
