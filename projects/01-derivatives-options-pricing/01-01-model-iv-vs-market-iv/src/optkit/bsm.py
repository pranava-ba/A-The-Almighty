"""Black-Scholes-Merton pricing and the full Greek set (continuous dividend yield q).

Everything here is vectorised: ``S, K, t, r, sigma, q`` may be Python scalars or
NumPy arrays and broadcast together, so a whole option chain prices in one call.
Conventions, fixed once and used everywhere downstream:

* ``kind`` is ``"call"`` or ``"put"`` (case-insensitive), or an array of those.
* ``vega``  = ∂V/∂σ  per **1.00** of vol (i.e. per 100 vol-points); divide by 100
  for the "per 1 vol-point" number traders quote.
* ``theta`` = **calendar** decay = −∂V/∂(time-to-expiry) per **year** (so it is
  negative for most long options); divide by 365 for per-calendar-day decay.
* ``rho``   = ∂V/∂r  per **1.00** of rate (per 100 bp × 100).

Degenerate inputs are handled rather than warned about: at ``t <= 0`` an option is
worth its intrinsic value and its second-order Greeks vanish; at ``sigma <= 0`` the
price collapses to the discounted forward intrinsic ``max(φ(S e^{-qt} - K e^{-rt}), 0)``.
"""
from __future__ import annotations

import numpy as np
from scipy.stats import norm

__all__ = ["d1_d2", "bsm_price", "delta", "gamma", "vega", "theta", "rho", "greeks"]

_N = norm.cdf
_n = norm.pdf


def _phi(kind):
    """Map ``kind`` to the option sign φ: +1 for a call, -1 for a put."""
    if isinstance(kind, str):
        k = kind.lower()
        if k in ("c", "call"):
            return 1.0
        if k in ("p", "put"):
            return -1.0
        raise ValueError(f"kind must be 'call' or 'put', got {kind!r}")
    arr = np.asarray(kind)
    out = np.empty(arr.shape, dtype=float)
    lower = np.char.lower(arr.astype(str))
    is_call = np.isin(lower, ("c", "call"))
    is_put = np.isin(lower, ("p", "put"))
    if not np.all(is_call | is_put):
        raise ValueError("kind array must contain only 'call'/'put'")
    out[is_call] = 1.0
    out[is_put] = -1.0
    return out


def d1_d2(S, K, t, r, sigma, q=0.0):
    """The Black-Scholes ``d1, d2`` terms (NaN where ``sigma*sqrt(t) == 0``)."""
    S, K, t, r, sigma, q = np.broadcast_arrays(
        *[np.asarray(x, dtype=float) for x in (S, K, t, r, sigma, q)]
    )
    vol_t = sigma * np.sqrt(t)
    with np.errstate(divide="ignore", invalid="ignore"):
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * t) / vol_t
        d2 = d1 - vol_t
    return d1, d2


def _forward_intrinsic(S, K, t, r, q, phi):
    """σ→0 limit: the payoff on the discounted forward, floored at zero."""
    return np.maximum(phi * (S * np.exp(-q * t) - K * np.exp(-r * t)), 0.0)


def bsm_price(S, K, t, r, sigma, q=0.0, kind="call"):
    """Black-Scholes-Merton option price. Scalars in → scalar out; arrays broadcast."""
    S, K, t, r, sigma, q = [np.asarray(x, dtype=float) for x in (S, K, t, r, sigma, q)]
    phi = _phi(kind)
    S, K, t, r, sigma, q, phi = np.broadcast_arrays(S, K, t, r, sigma, q, phi)

    live = (t > 0) & (sigma > 0)
    d1, d2 = d1_d2(S, K, t, r, sigma, q)
    disc_S = S * np.exp(-q * t)
    disc_K = K * np.exp(-r * t)
    priced = phi * (disc_S * _N(phi * d1) - disc_K * _N(phi * d2))

    out = np.where(live, priced, _forward_intrinsic(S, K, t, r, q, phi))
    return out if out.ndim else out.item()


def delta(S, K, t, r, sigma, q=0.0, kind="call"):
    """∂V/∂S. Call ∈ (0, e^{-qt}); put ∈ (-e^{-qt}, 0)."""
    S, K, t, r, sigma, q = [np.asarray(x, dtype=float) for x in (S, K, t, r, sigma, q)]
    phi = _phi(kind)
    S, K, t, r, sigma, q, phi = np.broadcast_arrays(S, K, t, r, sigma, q, phi)
    live = (t > 0) & (sigma > 0)
    d1, _ = d1_d2(S, K, t, r, sigma, q)
    val = phi * np.exp(-q * t) * _N(phi * d1)
    # σ→0 / expiry: delta is the (discounted) exercise indicator.
    itm = phi * (S * np.exp(-q * t) - K * np.exp(-r * t)) > 0
    out = np.where(live, val, np.where(itm, phi * np.exp(-q * t), 0.0))
    return out if out.ndim else out.item()


def gamma(S, K, t, r, sigma, q=0.0, kind="call"):
    """∂²V/∂S² (identical for calls and puts)."""
    S, K, t, r, sigma, q = np.broadcast_arrays(
        *[np.asarray(x, dtype=float) for x in (S, K, t, r, sigma, q)]
    )
    live = (t > 0) & (sigma > 0)
    d1, _ = d1_d2(S, K, t, r, sigma, q)
    with np.errstate(divide="ignore", invalid="ignore"):
        val = np.exp(-q * t) * _n(d1) / (S * sigma * np.sqrt(t))
    out = np.where(live, val, 0.0)
    return out if out.ndim else out.item()


def vega(S, K, t, r, sigma, q=0.0, kind="call"):
    """∂V/∂σ per 1.00 of vol (identical for calls and puts)."""
    S, K, t, r, sigma, q = np.broadcast_arrays(
        *[np.asarray(x, dtype=float) for x in (S, K, t, r, sigma, q)]
    )
    live = (t > 0) & (sigma > 0)
    d1, _ = d1_d2(S, K, t, r, sigma, q)
    val = S * np.exp(-q * t) * _n(d1) * np.sqrt(t)
    out = np.where(live, val, 0.0)
    return out if out.ndim else out.item()


def theta(S, K, t, r, sigma, q=0.0, kind="call"):
    """Calendar theta = −∂V/∂(time-to-expiry) per year (divide by 365 for per-day)."""
    S, K, t, r, sigma, q = [np.asarray(x, dtype=float) for x in (S, K, t, r, sigma, q)]
    phi = _phi(kind)
    S, K, t, r, sigma, q, phi = np.broadcast_arrays(S, K, t, r, sigma, q, phi)
    live = (t > 0) & (sigma > 0)
    d1, d2 = d1_d2(S, K, t, r, sigma, q)
    disc_S = S * np.exp(-q * t)
    disc_K = K * np.exp(-r * t)
    with np.errstate(divide="ignore", invalid="ignore"):
        carry = -disc_S * _n(d1) * sigma / (2.0 * np.sqrt(t))
    val = carry - phi * r * disc_K * _N(phi * d2) + phi * q * disc_S * _N(phi * d1)
    out = np.where(live, val, 0.0)
    return out if out.ndim else out.item()


def rho(S, K, t, r, sigma, q=0.0, kind="call"):
    """∂V/∂r per 1.00 of rate."""
    S, K, t, r, sigma, q = [np.asarray(x, dtype=float) for x in (S, K, t, r, sigma, q)]
    phi = _phi(kind)
    S, K, t, r, sigma, q, phi = np.broadcast_arrays(S, K, t, r, sigma, q, phi)
    live = (t > 0) & (sigma > 0)
    _, d2 = d1_d2(S, K, t, r, sigma, q)
    val = phi * K * t * np.exp(-r * t) * _N(phi * d2)
    out = np.where(live, val, 0.0)
    return out if out.ndim else out.item()


def greeks(S, K, t, r, sigma, q=0.0, kind="call"):
    """All five Greeks + price as a dict of arrays (or scalars). One BSM eval each."""
    return {
        "price": bsm_price(S, K, t, r, sigma, q, kind),
        "delta": delta(S, K, t, r, sigma, q, kind),
        "gamma": gamma(S, K, t, r, sigma, q, kind),
        "vega": vega(S, K, t, r, sigma, q, kind),
        "theta": theta(S, K, t, r, sigma, q, kind),
        "rho": rho(S, K, t, r, sigma, q, kind),
    }
