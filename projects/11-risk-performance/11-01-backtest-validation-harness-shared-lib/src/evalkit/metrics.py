"""Performance metrics — the shared tearsheet every strategy reports through.

The point of the lab: no strategy is judged on a raw Sharpe. Everything is net-of-cost and
run through the same screen, and a headline Sharpe is discounted for skew, kurtosis, sample
length, and — via the Deflated Sharpe — the number of configurations tried.
"""
from __future__ import annotations

import numpy as np
from scipy.stats import kurtosis, norm, skew

_EULER = 0.5772156649015329


def sharpe(returns, periods_per_year: int = 252, rf: float = 0.0) -> float:
    r = np.asarray(returns, float)
    if len(r) < 2:
        return float("nan")
    ex = r - rf / periods_per_year
    sd = ex.std(ddof=1)
    return float("nan") if sd == 0 else float(ex.mean() / sd * np.sqrt(periods_per_year))


def max_drawdown(returns) -> float:
    r = np.asarray(returns, float)
    if len(r) == 0:
        return 0.0
    eq = np.cumprod(1 + r)
    return float((eq / np.maximum.accumulate(eq) - 1).min())


def _sr_per_period(r: np.ndarray) -> float:
    sd = r.std(ddof=1)
    return 0.0 if sd == 0 else float(r.mean() / sd)


def probabilistic_sharpe(returns, sr_benchmark: float = 0.0) -> float:
    """PSR: P(true per-period SR > benchmark), correcting for skew/kurtosis & sample size."""
    r = np.asarray(returns, float)
    n = len(r)
    if n < 3:
        return float("nan")
    sr = _sr_per_period(r)
    s, k = float(skew(r)), float(kurtosis(r, fisher=False))  # kurtosis non-excess
    den = np.sqrt(max(1e-12, 1 - s * sr + (k - 1) / 4 * sr ** 2))
    return float(norm.cdf((sr - sr_benchmark) * np.sqrt(n - 1) / den))


def deflated_sharpe(returns, sr_trials_std: float, n_trials: int) -> float:
    """DSR: PSR against the Sharpe you'd expect as the MAX of `n_trials` random configs —
    i.e. the headline Sharpe discounted for selection bias (Bailey & López de Prado)."""
    r = np.asarray(returns, float)
    if n_trials < 2 or sr_trials_std <= 0:
        return probabilistic_sharpe(r, 0.0)
    sr0 = sr_trials_std * ((1 - _EULER) * norm.ppf(1 - 1 / n_trials)
                           + _EULER * norm.ppf(1 - 1 / (n_trials * np.e)))
    return probabilistic_sharpe(r, sr0)


def turnover(weights) -> float:
    """Mean per-period gross change in weights (sum |Δw|)."""
    W = np.atleast_2d(np.asarray(weights, float))
    if W.shape[0] == 1:
        W = W.T
    return 0.0 if len(W) < 2 else float(np.abs(np.diff(W, axis=0)).sum(axis=1).mean())


def net_returns(gross, costs):
    return np.asarray(gross, float) - np.asarray(costs, float)


def tearsheet(returns, periods_per_year: int = 252, n_trials: int = 1,
              sr_trials_std: float = 0.0) -> dict:
    r = np.asarray(returns, float)
    n = len(r)
    out = {
        "n": int(n),
        "ann_return": float(np.prod(1 + r) ** (periods_per_year / n) - 1) if n else 0.0,
        "sharpe": sharpe(r, periods_per_year),
        "max_drawdown": max_drawdown(r),
        "psr": probabilistic_sharpe(r, 0.0),
        "hit_rate": float((r > 0).mean()) if n else 0.0,
    }
    if n_trials > 1:
        out["deflated_sharpe"] = deflated_sharpe(r, sr_trials_std, n_trials)
    return out
