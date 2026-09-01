"""Offline tests for the tape recorder/replay and point-in-time / corporate-action layer."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from datalake import (  # noqa: E402
    PointInTimeUniverse, TapeRecorder, TapeReplay, adjust_candles,
)


def test_tape_roundtrip_and_order(tmp_path):
    p = tmp_path / "tape.ndjson"
    with TapeRecorder(p) as rec:
        rec.record([{"ts": 3, "ltp": 102}, {"ts": 1, "ltp": 100}, {"ts": 2, "ltp": 101}])
    evs = TapeReplay(p).events(sort=True)
    assert [e["ts"] for e in evs] == [1, 2, 3]          # deterministic order
    assert [e["ltp"] for e in evs] == [100, 101, 102]


def test_tape_gzip(tmp_path):
    p = tmp_path / "tape.ndjson.gz"
    with TapeRecorder(p) as rec:
        assert rec.record([{"ts": 1, "x": "a"}]) == 1
    assert list(TapeReplay(p)) == [{"ts": 1, "x": "a"}]


def _membership():
    return pd.DataFrame([
        {"index": "NIFTY50", "symbol": "RELIANCE", "start": "2018-01-01", "end": None},
        {"index": "NIFTY50", "symbol": "YESBANK", "start": "2018-01-01", "end": "2020-03-27"},
        {"index": "NIFTY50", "symbol": "SBILIFE", "start": "2020-03-27", "end": None},
    ])


def test_point_in_time_membership():
    u = PointInTimeUniverse(_membership())
    assert u.members_asof("NIFTY50", "2019-06-01") == ["RELIANCE", "YESBANK"]
    assert u.members_asof("NIFTY50", "2021-01-01") == ["RELIANCE", "SBILIFE"]  # survivorship-safe


def test_corporate_action_backadjust():
    df = pd.DataFrame({
        "ts": pd.to_datetime(["2026-01-01", "2026-02-01", "2026-03-01"]),
        "open": [200.0, 210.0, 105.0], "high": [200, 210, 105], "low": [200, 210, 105],
        "close": [200.0, 210.0, 105.0],
    })
    actions = pd.DataFrame([{"ex_date": "2026-02-15", "factor": 0.5}])  # 1:2 split on Feb 15
    adj = adjust_candles(df, actions)
    # bars BEFORE ex-date halved; the post-split bar unchanged → continuous ~100/105/105
    assert adj.loc[0, "close"] == 100.0
    assert adj.loc[1, "close"] == 105.0
    assert adj.loc[2, "close"] == 105.0
