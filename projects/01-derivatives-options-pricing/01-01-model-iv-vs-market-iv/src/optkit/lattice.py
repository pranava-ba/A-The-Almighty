"""Lattice pricers — Cox-Ross-Rubinstein binomial and Boyle trinomial trees.

Both price European **and** American exercise under the same risk-neutral measure as
:mod:`optkit.bsm`, and both converge to the closed-form BSM price as ``n_steps → ∞``
(that convergence is a test). The American path adds an early-exercise check at every
node, so ``american_price ≥ european_price`` always, with the gap being the
early-exercise premium (non-zero mainly for American puts and deep-ITM dividend calls).

Pricers are scalar in ``S, K, t, r, sigma, q`` (one option per call); price a chain by
mapping over rows. Backward induction is vectorised across nodes within each tree, so a
few-hundred-step tree is cheap.
"""
from __future__ import annotations

import numpy as np

from .bsm import _phi

__all__ = ["crr_price", "trinomial_price"]


def crr_price(S, K, t, r, sigma, q=0.0, kind="call", n_steps=256, american=False):
    """Cox-Ross-Rubinstein binomial price.

    ``u = e^{σ√Δt}``, ``d = 1/u``, risk-neutral ``p = (e^{(r-q)Δt} - d)/(u - d)``.
    """
    S, K, t, r, sigma, q = (float(x) for x in (S, K, t, r, sigma, q))
    phi = _phi(kind)
    if t <= 0 or sigma <= 0:
        return max(phi * (S * np.exp(-q * t) - K * np.exp(-r * t)), 0.0)

    dt = t / n_steps
    u = np.exp(sigma * np.sqrt(dt))
    d = 1.0 / u
    disc = np.exp(-r * dt)
    p = (np.exp((r - q) * dt) - d) / (u - d)
    if not (0.0 <= p <= 1.0):                     # guard: Δt too coarse for this σ
        raise ValueError("CRR risk-neutral p outside [0,1]; increase n_steps")

    # Terminal asset prices S·u^j·d^(N-j) = S·d^N·(u/d)^j for j = 0..N.
    j = np.arange(n_steps + 1)
    prices = S * (d ** n_steps) * (u / d) ** j
    values = np.maximum(phi * (prices - K), 0.0)

    for i in range(n_steps, 0, -1):
        values = disc * (p * values[1:i + 1] + (1.0 - p) * values[0:i])
        if american:
            prices = prices[:i] / d                # node prices one step earlier
            values = np.maximum(values, phi * (prices - K))
    return float(values[0])


def trinomial_price(S, K, t, r, sigma, q=0.0, kind="call", n_steps=128, american=False):
    """Boyle trinomial price (up / flat / down), stable for the usual equity regime.

    Uses ``u = e^{σ√(2Δt)}``, ``m = 1``, ``d = 1/u`` with Boyle's probabilities, which
    converges to BSM faster per step than the binomial for smooth (European) payoffs.
    """
    S, K, t, r, sigma, q = (float(x) for x in (S, K, t, r, sigma, q))
    phi = _phi(kind)
    if t <= 0 or sigma <= 0:
        return max(phi * (S * np.exp(-q * t) - K * np.exp(-r * t)), 0.0)

    dt = t / n_steps
    u = np.exp(sigma * np.sqrt(2.0 * dt))
    d = 1.0 / u
    disc = np.exp(-r * dt)
    a = np.exp((r - q) * dt / 2.0)
    b_up = np.exp(sigma * np.sqrt(dt / 2.0))
    b_dn = np.exp(-sigma * np.sqrt(dt / 2.0))
    pu = ((a - b_dn) / (b_up - b_dn)) ** 2
    pd = ((b_up - a) / (b_up - b_dn)) ** 2
    pm = 1.0 - pu - pd
    if min(pu, pm, pd) < 0.0:                      # guard: Δt too coarse for this σ
        raise ValueError("trinomial probabilities went negative; increase n_steps")

    # Terminal nodes: S·u^k for k = -N..N (u^k with u>1, d=1/u).
    k = np.arange(-n_steps, n_steps + 1)
    prices = S * u ** k
    values = np.maximum(phi * (prices - K), 0.0)

    for i in range(n_steps, 0, -1):
        # Node k at step i-1 draws from up=k+1, mid=k, down=k-1 at step i.
        values = disc * (pu * values[2:] + pm * values[1:-1] + pd * values[:-2])
        if american:
            k = np.arange(-(i - 1), i)
            prices = S * u ** k
            values = np.maximum(values, phi * (prices - K))
    return float(values[0])
