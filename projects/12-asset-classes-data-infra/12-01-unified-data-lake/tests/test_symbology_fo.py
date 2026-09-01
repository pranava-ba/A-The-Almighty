"""Offline tests for the F&O bhavcopy parser and the symbology normalizer."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from datalake import COLUMNS, Symbology  # noqa: E402
from datalake.sources import NSEBhavcopySource  # noqa: E402


def _udiff_fo():
    return pd.DataFrame({
        "TradDt": ["2026-08-27"] * 3,
        "TckrSymb": ["NIFTY", "NIFTY", "NIFTY"],
        "XpryDt": ["2026-08-28", "2026-08-28", "2026-08-28"],
        "StrkPric": [0.0, 24200.0, 24200.0],
        "OptnTp": ["", "CE", "PE"],
        "OpnPric": [24250, 120, 90], "HghPric": [24300, 140, 100],
        "LwPric": [24200, 110, 80], "ClsPric": [24280, 130, 85],
        "TtlTradgVol": [100000, 50000, 40000], "OpnIntrst": [1000000, 250000, 300000],
    })


def test_parse_fo_keys_and_oi():
    out = NSEBhavcopySource._parse_fo(_udiff_fo())
    assert list(out.columns) == COLUMNS
    keys = list(out["instrument_key"])
    assert "NSE_FO|NIFTY|2026-08-28|FUT" in keys                     # future
    assert "NSE_FO|NIFTY|2026-08-28|24200.0|CE" in keys              # call option
    assert (out["oi"] > 0).all()                                    # OI populated
    assert out.loc[out["instrument_key"].str.endswith("PE"), "oi"].iloc[0] == 300000


# --- symbology ---
_INSTRS = [
    {"segment": "NSE_EQ", "trading_symbol": "RELIANCE", "isin": "INE002A01018",
     "instrument_key": "NSE_EQ|INE002A01018"},
    {"segment": "NSE_INDEX", "trading_symbol": "Nifty 50", "isin": None,
     "instrument_key": "NSE_INDEX|Nifty 50"},
]


def test_symbology_symbol_isin_key():
    s = Symbology(_INSTRS)
    assert s.upstox_key("RELIANCE") == "NSE_EQ|INE002A01018"
    assert s.isin("RELIANCE") == "INE002A01018"
    assert s.symbol_of_isin("INE002A01018") == "RELIANCE"
    assert s.upstox_key("NADA") is None


def test_symbology_yahoo():
    assert Symbology.yahoo("RELIANCE") == "RELIANCE.NS"
    assert Symbology.yahoo("TCS", "BSE_EQ") == "TCS.BO"
    assert Symbology.yahoo("NIFTY 50") == "^NSEI"
    assert Symbology.yahoo("SENSEX", "BSE_INDEX") == "^BSESN"
