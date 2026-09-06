"""Lattice pricers — convergence to BSM and the American early-exercise ordering."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from optkit import bsm_price, crr_price, trinomial_price  # noqa: E402

S, K, T, R, Q, SIG = 100.0, 100.0, 0.5, 0.05, 0.0, 0.20


def test_crr_converges_to_bsm():
    for kind in ("call", "put"):
        ref = bsm_price(S, K, T, R, SIG, Q, kind)
        assert abs(crr_price(S, K, T, R, SIG, Q, kind, n_steps=1024) - ref) < 0.02


def test_trinomial_converges_to_bsm():
    for kind in ("call", "put"):
        ref = bsm_price(S, K, T, R, SIG, Q, kind)
        assert abs(trinomial_price(S, K, T, R, SIG, Q, kind, n_steps=400) - ref) < 0.01


def test_more_steps_reduce_error():
    ref = bsm_price(S, K, T, R, SIG, Q, "call")
    coarse = abs(crr_price(S, K, T, R, SIG, Q, "call", n_steps=32) - ref)
    fine = abs(crr_price(S, K, T, R, SIG, Q, "call", n_steps=1024) - ref)
    assert fine < coarse


def test_american_ge_european():
    for kind in ("call", "put"):
        eu = crr_price(S, K, T, R, SIG, Q, kind, n_steps=400, american=False)
        am = crr_price(S, K, T, R, SIG, Q, kind, n_steps=400, american=True)
        assert am >= eu - 1e-9


def test_american_call_no_dividend_equals_european():
    # With q=0 an American call is never optimally exercised early -> equals European.
    eu = crr_price(S, K, T, R, SIG, 0.0, "call", n_steps=400, american=False)
    am = crr_price(S, K, T, R, SIG, 0.0, "call", n_steps=400, american=True)
    assert abs(am - eu) < 1e-6


def test_american_put_has_early_exercise_premium():
    # Deep ITM American put with a positive rate carries a real early-exercise premium.
    eu = crr_price(80.0, 100.0, 1.0, 0.08, 0.30, 0.0, "put", n_steps=600, american=False)
    am = crr_price(80.0, 100.0, 1.0, 0.08, 0.30, 0.0, "put", n_steps=600, american=True)
    assert am - eu > 0.10


def test_trinomial_american_agrees_with_binomial():
    for kind in ("call", "put"):
        b = crr_price(90, 100, 0.75, 0.06, 0.25, 0.0, kind, n_steps=500, american=True)
        t = trinomial_price(90, 100, 0.75, 0.06, 0.25, 0.0, kind, n_steps=300, american=True)
        assert abs(b - t) < 0.05
