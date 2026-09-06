"""BSM price + Greeks — offline, analytic checks and finite-difference Greek validation."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from optkit import bsm_price, delta, gamma, greeks, rho, theta, vega  # noqa: E402
from optkit.bsm import _phi  # noqa: E402

S, K, T, R, Q, SIG = 100.0, 100.0, 0.5, 0.05, 0.01, 0.20


def test_put_call_parity():
    c = bsm_price(S, K, T, R, SIG, Q, "call")
    p = bsm_price(S, K, T, R, SIG, Q, "put")
    lhs = c - p
    rhs = S * np.exp(-Q * T) - K * np.exp(-R * T)
    assert abs(lhs - rhs) < 1e-10


def test_price_increases_with_vol():
    lo = bsm_price(S, K, T, R, 0.10, Q, "call")
    hi = bsm_price(S, K, T, R, 0.40, Q, "call")
    assert hi > lo > 0


def test_delta_bounds_and_sign():
    dc = delta(S, K, T, R, SIG, Q, "call")
    dp = delta(S, K, T, R, SIG, Q, "put")
    assert 0.0 < dc < np.exp(-Q * T)
    assert -np.exp(-Q * T) < dp < 0.0
    # call - put delta = e^{-qt}
    assert abs((dc - dp) - np.exp(-Q * T)) < 1e-10


def test_gamma_vega_kind_independent():
    assert abs(gamma(S, K, T, R, SIG, Q, "call") - gamma(S, K, T, R, SIG, Q, "put")) < 1e-12
    assert abs(vega(S, K, T, R, SIG, Q, "call") - vega(S, K, T, R, SIG, Q, "put")) < 1e-12


def _fd(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)


def test_greeks_match_finite_difference():
    for kind in ("call", "put"):
        d_fd = _fd(lambda s: bsm_price(s, K, T, R, SIG, Q, kind), S, 1e-3)
        assert abs(delta(S, K, T, R, SIG, Q, kind) - d_fd) < 1e-6

        g_fd = (bsm_price(S + 1e-2, K, T, R, SIG, Q, kind)
                - 2 * bsm_price(S, K, T, R, SIG, Q, kind)
                + bsm_price(S - 1e-2, K, T, R, SIG, Q, kind)) / 1e-4
        assert abs(gamma(S, K, T, R, SIG, Q, kind) - g_fd) < 1e-4

        v_fd = _fd(lambda v: bsm_price(S, K, T, R, v, Q, kind), SIG, 1e-4)
        assert abs(vega(S, K, T, R, SIG, Q, kind) - v_fd) < 1e-4

        # theta is CALENDAR decay = -∂V/∂(time-to-expiry); the FD is +∂V/∂ttm.
        dv_dttm = _fd(lambda tt: bsm_price(S, K, tt, R, SIG, Q, kind), T, 1e-5)
        assert abs(theta(S, K, T, R, SIG, Q, kind) - (-dv_dttm)) < 1e-3

        r_fd = _fd(lambda rr: bsm_price(S, K, T, rr, SIG, Q, kind), R, 1e-5)
        assert abs(rho(S, K, T, R, SIG, Q, kind) - r_fd) < 1e-4


def test_degenerate_expiry_and_zero_vol():
    # t -> 0: intrinsic
    assert abs(bsm_price(110, 100, 0.0, R, SIG, 0.0, "call") - 10.0) < 1e-12
    assert bsm_price(90, 100, 0.0, R, SIG, 0.0, "call") == 0.0
    # sigma -> 0: discounted forward intrinsic
    fwd_call = max(105 * np.exp(-Q * T) - 100 * np.exp(-R * T), 0.0)
    assert abs(bsm_price(105, 100, T, R, 0.0, Q, "call") - fwd_call) < 1e-12


def test_vectorised_broadcast():
    ks = np.array([90.0, 100.0, 110.0])
    out = bsm_price(S, ks, T, R, SIG, Q, "call")
    assert out.shape == (3,)
    assert np.all(np.diff(out) < 0)          # lower strike -> pricier call
    g = greeks(S, ks, T, R, SIG, Q, "call")
    assert g["delta"].shape == (3,) and np.all(np.diff(g["delta"]) < 0)


def test_phi_rejects_bad_kind():
    try:
        _phi("banana")
    except ValueError:
        return
    raise AssertionError("expected ValueError for bad kind")
