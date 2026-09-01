"""Offline test for the NSE bhavcopy parser — synthetic UDiFF frame, no network."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from datalake import COLUMNS  # noqa: E402
from datalake.sources import NSEBhavcopySource  # noqa: E402


def _udiff_cm():
    return pd.DataFrame({
        "TradDt": ["2026-08-27", "2026-08-27", "2026-08-27"],
        "TckrSymb": ["RELIANCE", "TCS", "NIFTY"],
        "FinInstrmTp": ["STK", "STK", "IDX"],
        "OpnPric": [1400.0, 3100.0, 24200.0], "HghPric": [1420.0, 3130.0, 24300.0],
        "LwPric": [1390.0, 3080.0, 24100.0], "ClsPric": [1410.0, 3120.0, 24250.0],
        "TtlTradgVol": [1000000, 500000, 0],
    })


def test_parse_cm_filters_equity_and_symbol():
    out = NSEBhavcopySource._parse_cm(_udiff_cm(), symbol="RELIANCE")
    assert list(out.columns) == COLUMNS
    assert len(out) == 1
    assert out["instrument_key"].iloc[0] == "NSE_EQ|RELIANCE"
    assert out["close"].iloc[0] == 1410.0
    assert out["source"].iloc[0] == "nse_bhavcopy"
    assert pd.isna(out["oi"].iloc[0])                       # equity bhavcopy has no OI
    assert out["ts"].iloc[0].utcoffset() == pd.Timedelta(hours=5, minutes=30)


def test_parse_cm_drops_index_rows():
    out = NSEBhavcopySource._parse_cm(_udiff_cm())          # no symbol filter
    assert set(out["instrument_key"]) == {"NSE_EQ|RELIANCE", "NSE_EQ|TCS"}  # IDX dropped


def test_nse_registered_and_rejects_intraday():
    from datalake.sources import available
    assert "nse_bhavcopy" in available()
    try:
        NSEBhavcopySource().candles("RELIANCE", "1minute")
        assert False, "should reject intraday"
    except ValueError:
        pass
