"""Implied-vol inversion — round-trip recovery, the Brent fallback, and no-arb guards."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from optkit import bsm_price, implied_vol, implied_vol_chain  # noqa: E402
from optkit.iv import SIGMA_MAX  # noqa: E402

S, T, R, Q = 100.0, 0.5, 0.05, 0.01


def test_round_trip_recovers_sigma():
    for kind in ("call", "put"):
        for K in (80, 95, 100, 105, 120):
            for sig in (0.08, 0.20, 0.55):
                px = bsm_price(S, K, T, R, sig, Q, kind)
                got = implied_vol(px, S, K, T, R, Q, kind)
                assert abs(got - sig) < 1e-6, (kind, K, sig, got)


def test_deep_wing_uses_fallback_but_recovers():
    # Deep OTM: tiny price, vega near zero -> exercises the Brent branch.
    K, sig = 160.0, 0.35
    px = bsm_price(S, K, T, R, sig, Q, "call")
    got = implied_vol(px, S, K, T, R, Q, "call")
    assert abs(got - sig) < 1e-4


def test_intrinsic_price_is_zero_vol():
    intrinsic = max(105 * np.exp(-Q * T) - 100 * np.exp(-R * T), 0.0)
    assert implied_vol(intrinsic, 105, 100, T, R, Q, "call") == 0.0


def test_arbitrage_prices_return_nan():
    # Below intrinsic and above the upper bound both have no real IV.
    assert np.isnan(implied_vol(-1.0, S, 100, T, R, Q, "call"))
    upper = S * np.exp(-Q * T)
    assert np.isnan(implied_vol(upper + 1.0, S, 100, T, R, Q, "call"))


def test_on_fail_raise():
    try:
        implied_vol(1e9, S, 100, T, R, Q, "call", on_fail="raise")
    except ValueError:
        return
    raise AssertionError("expected ValueError with on_fail='raise'")


def test_chain_is_vectorised_and_nan_safe():
    K = np.array([90.0, 100.0, 110.0, 100.0])
    sig = np.array([0.25, 0.20, 0.30, 0.20])
    px = bsm_price(S, K, T, R, sig, Q, "call")
    px = px.copy()
    px[3] = -5.0                                   # one poisoned quote
    out = implied_vol_chain(px, S, K, T, R, Q, "call")
    assert out.shape == (4,)
    assert np.allclose(out[:3], sig[:3], atol=1e-6)
    assert np.isnan(out[3])                         # bad row -> NaN, no raise


def test_high_vol_within_band():
    px = bsm_price(S, 100, T, R, 2.5, Q, "call")
    got = implied_vol(px, S, 100, T, R, Q, "call")
    assert abs(got - 2.5) < 1e-4 and got < SIGMA_MAX
