"""Offline tests for cross-source reconciliation."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from datalake import COLUMNS, bad_print_mask, normalize, reconcile  # noqa: E402


def _frame(closes, source, start="2026-08-27 09:15"):
    ts = pd.date_range(start, periods=len(closes), freq="1min", tz="Asia/Kolkata")
    raw = pd.DataFrame({"ts": ts, "open": closes, "high": [c + 1 for c in closes],
                        "low": [c - 1 for c in closes], "close": closes,
                        "volume": 100})
    return normalize(raw, "NSE_INDEX|Nifty 50", "1minute", source)


def test_bad_print_mask():
    df = normalize(pd.DataFrame({"ts": ["2026-08-27 09:15", "2026-08-27 09:16"],
                                 "open": [100, 100], "high": [99, 101],  # first: high<low → bad
                                 "low": [100, 99], "close": [100, 100], "volume": [1, 1]}),
                   "X", "1minute", "s")
    assert bad_print_mask(df).tolist() == [True, False]


def test_reconcile_gapfill_and_mismatch():
    a = _frame([100, 101, 102], "yfinance")                 # 3 bars
    b = _frame([100, 999, 102, 103], "nse_bhavcopy")        # extra 4th bar (gap-fill) + bar2 mismatch
    merged, sc = reconcile({"yfinance": a, "nse_bhavcopy": b}, primary="yfinance")
    assert list(merged.columns) == COLUMNS
    assert sc["merged_rows"] == 4                            # 3 + 1 filled from b
    assert sc["cross_source_mismatches"] == 1               # bar2 close 101 vs 999
    assert sc["coverage"]["yfinance"] == 0.75               # 3 of 4 union ts
    # the gap-filled 4th bar carries b's source tag
    assert merged.iloc[-1]["source"] == "nse_bhavcopy"


def test_reconcile_counts_bad_prints():
    good = _frame([100, 101], "a")
    bad = good.copy()
    bad.loc[0, "high"] = 1.0                                 # high < low → bad print
    _, sc = reconcile({"a": good, "b": bad})
    assert sc["sources"]["b"]["bad_prints"] == 1
