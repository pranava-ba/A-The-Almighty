"""Implied-volatility inversion: recover σ from a market price.

The workhorse is Newton-Raphson on ``f(σ) = bsm_price(σ) - price`` using ``vega`` as the
derivative — quadratically convergent where vega is healthy (near-ATM, not near expiry).
Two things make it production-safe rather than a textbook one-liner:

* **No-arbitrage screening first.** A price at/below intrinsic implies σ = 0; a price
  above the trivial upper bound (``S e^{-qt}`` for a call, ``K e^{-rt}`` for a put) has no
  real IV — we return ``NaN`` with the reason rather than diverging.
* **Brent fallback.** Deep ITM/OTM or near-expiry vega collapses and Newton stalls or
  overshoots; we then bracket-solve with :func:`scipy.optimize.brentq`, which cannot
  leave the ``[σ_lo, σ_hi]`` interval.

``implied_vol`` is scalar; ``implied_vol_chain`` maps it over arrays and returns ``NaN``
for rows that fail rather than raising, so one bad quote never sinks a whole surface.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.optimize import brentq

from .bsm import _phi, bsm_price, vega

__all__ = ["implied_vol", "implied_vol_chain", "SIGMA_MIN", "SIGMA_MAX"]

SIGMA_MIN = 1e-6
SIGMA_MAX = 5.0            # 500% annualised — nothing liquid trades above this


def _bounds(S, K, t, r, q, phi):
    """(lower, upper) no-arb price bounds for this option."""
    lower = max(phi * (S * math.exp(-q * t) - K * math.exp(-r * t)), 0.0)
    upper = S * math.exp(-q * t) if phi > 0 else K * math.exp(-r * t)
    return lower, upper


def implied_vol(price, S, K, t, r, q=0.0, kind="call",
                tol=1e-8, max_iter=100, on_fail="nan"):
    """Implied vol of a single option, or ``NaN``/raise if it has none.

    ``on_fail`` is ``"nan"`` (default) or ``"raise"``.
    """
    price, S, K, t, r, q = (float(x) for x in (price, S, K, t, r, q))
    phi = _phi(kind)

    def _fail(msg):
        if on_fail == "raise":
            raise ValueError(msg)
        return float("nan")

    if t <= 0 or S <= 0 or K <= 0:
        return _fail("non-positive t/S/K has no implied vol")

    lower, upper = _bounds(S, K, t, r, q, phi)
    if price < lower - 1e-10:
        return _fail(f"price {price} below intrinsic {lower}: arbitrage")
    if price <= lower + 1e-12:
        return 0.0                                  # exactly intrinsic → zero vol
    if price >= upper - 1e-12:
        return _fail(f"price {price} at/above upper bound {upper}: no real IV")

    # Brenner-Subrahmanyam ATM seed, clipped into the search band.
    sigma = max(SIGMA_MIN, min(SIGMA_MAX,
                math.sqrt(2 * math.pi / t) * price / S))
    for _ in range(max_iter):
        diff = bsm_price(S, K, t, r, sigma, q, kind) - price
        if abs(diff) < tol:
            return float(sigma)
        v = vega(S, K, t, r, sigma, q, kind)
        if v < 1e-8:
            break                                   # vega too flat → hand to Brent
        step = diff / v
        sigma -= step
        if not (SIGMA_MIN <= sigma <= SIGMA_MAX):
            break                                   # left the band → hand to Brent

    # Bracketed fallback: guaranteed on a sign change across the band.
    g = lambda s: bsm_price(S, K, t, r, s, q, kind) - price
    try:
        if g(SIGMA_MIN) * g(SIGMA_MAX) <= 0:
            return float(brentq(g, SIGMA_MIN, SIGMA_MAX, xtol=tol, maxiter=200))
    except (ValueError, RuntimeError):
        pass
    return _fail("Newton and Brent both failed to converge")


def implied_vol_chain(price, S, K, t, r, q=0.0, kind="call", **kw):
    """Vectorised :func:`implied_vol`; rows that fail return ``NaN`` (never raise)."""
    kw.setdefault("on_fail", "nan")
    price, S, K, t, r, q = np.broadcast_arrays(
        *[np.asarray(x, dtype=float) for x in (price, S, K, t, r, q)]
    )
    kind_arr = np.broadcast_to(np.asarray(kind), price.shape)
    out = np.empty(price.shape, dtype=float)
    it = np.nditer(price, flags=["multi_index"])
    for _ in it:
        i = it.multi_index
        out[i] = implied_vol(price[i], S[i], K[i], t[i], r[i], q[i], str(kind_arr[i]), **kw)
    return out if out.ndim else out.item()
