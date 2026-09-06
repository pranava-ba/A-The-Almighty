"""The model-vs-market IV surface — inversion recovery, method agreement, the smile."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from optkit import diff_surface, scorecard, synthetic_smile_chain  # noqa: E402
from optkit.chain import OptionChain, implied_spot_from_future  # noqa: E402
from optkit.surface import format_scorecard  # noqa: E402


def test_inversion_recovers_planted_smile():
    ch = synthetic_smile_chain(spot=100, r=0.05, q=0.0, ttms=(0.25, 0.5),
                               atm_vol=0.20, skew=-0.15, curv=0.60)
    df = diff_surface(ch, model_iv="atm")
    # market_iv inverted from price must equal the planted IV.
    assert np.max(np.abs(df["market_iv"].to_numpy() - ch.market_iv)) < 1e-6


def test_methods_agree_and_roundtrip_tight():
    ch = synthetic_smile_chain(ttms=(0.5,))
    sc = scorecard(diff_surface(ch, model_iv="atm"))
    assert sc["roundtrip_max"] < 1e-6            # BSM(IV) reprices the quote
    assert sc["method_max_abs"] < 0.05           # CRR & trinomial track BSM


def test_flat_model_reveals_equity_skew():
    ch = synthetic_smile_chain(ttms=(0.5,), atm_vol=0.20, skew=-0.15, curv=0.60)
    df = diff_surface(ch, model_iv="atm")
    k = np.log(df["strike"] / df["forward"]).to_numpy()
    iv_diff = df["iv_diff"].to_numpy()
    lower = iv_diff[k < -0.03].mean()            # downside puts
    upper = iv_diff[k > 0.03].mean()             # upside calls
    assert lower > upper                          # smirk: puts richer than calls vs flat
    assert abs(iv_diff[np.argmin(np.abs(k))]) < 1e-6   # ATM sits on the model


def test_scorecard_keys_and_formatting():
    ch = synthetic_smile_chain(ttms=(0.25,))
    sc = scorecard(diff_surface(ch))
    for key in ("iv_rmse", "price_rmse", "roundtrip_max", "method_max_abs",
                "put_call_iv_gap", "iv_rmse_by_region"):
        assert key in sc
    text = format_scorecard(sc)
    assert "IV RMSE" in text and "%" in text     # house-style block renders


def test_from_fo_frame_parses_option_rows():
    # A tiny canonical-schema F&O frame (as the data lake would hand us).
    df = _fo_frame()
    ch = OptionChain.from_fo_frame(df, spot=100.0, r=0.05, asof="2026-09-01")
    assert len(ch) == 2                           # the FUT row is skipped
    assert set(ch.kind) == {"call", "put"}
    assert np.allclose(sorted(ch.strike), [100.0, 105.0])


def test_implied_spot_from_future():
    S = implied_spot_from_future(101.0, t=0.25, r=0.05, q=0.0)
    # forward > spot when r>q, so the implied spot sits below the future price.
    assert S < 101.0
    assert abs(S - 101.0 * np.exp(-0.05 * 0.25)) < 1e-9


def _fo_frame():
    import pandas as pd
    keys = ["NSE_FO|NIFTY|2026-09-25|100|CE",
            "NSE_FO|NIFTY|2026-09-25|105|PE",
            "NSE_FO|NIFTY|2026-09-25|FUT"]
    return pd.DataFrame({
        "instrument_key": keys,
        "interval": "1day",
        "ts": pd.Timestamp("2026-09-01"),
        "close": [3.25, 6.10, 101.0],
        "oi": [1000, 800, 5000],
    })
