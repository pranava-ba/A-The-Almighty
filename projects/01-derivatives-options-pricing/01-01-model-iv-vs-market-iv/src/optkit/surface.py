"""The model-vs-market IV surface — the 01-01 deliverable.

Given an :class:`~optkit.chain.OptionChain` of market quotes, this layer answers three
questions across the whole strike × expiry grid:

1. **Market IV.** Invert each quote to its Black-Scholes implied vol (:mod:`optkit.iv`).
2. **Method agreement.** Re-price at that same IV with BSM, CRR and trinomial trees; the
   three must agree to a few basis points — a lattice that drifts is a bug, not a market.
3. **Model error = the smile.** Price the chain under a *single* model vol per expiry
   (flat BSM). The gap ``market_iv − model_iv`` is exactly the volatility smile/skew: the
   documented failure of the flat-vol model, laid out as a surface.

When a live Upstox chain is available (token, private path), the broker also publishes its
own IV and Greeks; :func:`attach_broker` diffs ours against theirs. Offline, all three
questions are answered from price alone, so the whole module runs with no token.

Display honours the house numeric style (§8): 6 decimals, comma thousands, signed %.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .bsm import greeks
from .chain import OptionChain
from .iv import implied_vol_chain
from .lattice import crr_price, trinomial_price

__all__ = ["model_surface", "diff_surface", "scorecard", "format_scorecard",
           "attach_broker"]


def _resolve_market_iv(chain: OptionChain) -> np.ndarray:
    """Market IV from the chain: use quoted IV where present, else invert the price."""
    if chain.market_iv is not None and not np.all(np.isnan(chain.market_iv)):
        return chain.market_iv.copy()
    return implied_vol_chain(chain.market_price, chain.spot, chain.strike,
                             chain.ttm, chain.r, chain.q, chain.kind)


def _model_iv(chain: OptionChain, market_iv, model_iv):
    """Resolve the *model* IV per row from ``model_iv``.

    * ``"atm"``  — flat per expiry at the ATM market vol (strike nearest the forward).
    * scalar     — one flat vol everywhere.
    * callable   — ``f(log_moneyness, ttm)`` evaluated per row (bring your own smile model).
    """
    if callable(model_iv):
        return np.array([model_iv(k, t) for k, t in zip(chain.log_moneyness, chain.ttm)])
    if model_iv == "atm":
        out = np.empty(len(chain))
        k = chain.log_moneyness
        for t in np.unique(chain.ttm):
            m = chain.ttm == t
            atm = market_iv[m][np.argmin(np.abs(k[m]))]     # vol at strike nearest F
            out[m] = atm
        return out
    return np.broadcast_to(float(model_iv), (len(chain),)).copy()


def model_surface(chain: OptionChain, model_iv="atm", crr_steps=256, tri_steps=128):
    """Per-row market IV, model IV, tri/BSM/CRR prices, and BSM Greeks at the market IV."""
    miv = _resolve_market_iv(chain)
    mdl = _model_iv(chain, miv, model_iv)
    S, K, t, r, q, cp = chain.spot, chain.strike, chain.ttm, chain.r, chain.q, chain.kind

    g = greeks(S, K, t, r, miv, q, cp)                       # Greeks on the market surface
    bsm_mkt = g["price"]                                     # BSM at market IV (round-trip)
    bsm_mdl = greeks(S, K, t, r, mdl, q, cp)["price"]        # BSM at the model IV
    crr = np.array([crr_price(S[i], K[i], t[i], r[i], miv[i], q[i], cp[i], crr_steps)
                    for i in range(len(chain))])
    tri = np.array([trinomial_price(S[i], K[i], t[i], r[i], miv[i], q[i], cp[i], tri_steps)
                    for i in range(len(chain))])

    out = chain.as_frame()
    out["market_iv"] = miv
    out["model_iv"] = mdl
    out["bsm_at_market"] = bsm_mkt
    out["crr_at_market"] = crr
    out["tri_at_market"] = tri
    out["bsm_at_model"] = bsm_mdl
    for gk in ("delta", "gamma", "vega", "theta", "rho"):
        out[gk] = g[gk]
    return out


def diff_surface(chain: OptionChain, model_iv="atm", **kw):
    """:func:`model_surface` + the diffs that make it a *comparison* surface."""
    df = model_surface(chain, model_iv=model_iv, **kw)
    df["iv_diff"] = df["market_iv"] - df["model_iv"]         # the smile, vs the model
    df["price_diff"] = df["market_price"] - df["bsm_at_model"]
    with np.errstate(divide="ignore", invalid="ignore"):
        df["price_diff_pct"] = np.where(df["market_price"] != 0,
                                        df["price_diff"] / df["market_price"], np.nan)
    df["crr_minus_bsm"] = df["crr_at_market"] - df["bsm_at_market"]
    df["tri_minus_bsm"] = df["tri_at_market"] - df["bsm_at_market"]
    return df


def _bucket(k):
    """Log-moneyness → coarse surface region."""
    return np.where(np.abs(k) < 0.03, "atm", np.where(k > 0, "upper", "lower"))


def _put_call_iv_gap(df: pd.DataFrame) -> float:
    """Max |IV_call − IV_put| across strikes quoted on both sides (parity sanity)."""
    gaps = []
    for (_, _), grp in df.groupby([df["ttm"].round(6), df["strike"].round(6)]):
        ivs = grp.groupby("kind")["market_iv"].mean()
        if {"call", "put"} <= set(ivs.index):
            gaps.append(abs(ivs["call"] - ivs["put"]))
    return float(max(gaps)) if gaps else float("nan")


def scorecard(diff_df: pd.DataFrame) -> dict:
    """Reduce a diff surface to the numbers that decide if the model/pricers are honest."""
    k = np.log(diff_df["strike"] / diff_df["forward"]).to_numpy()
    bucket = _bucket(k)
    iv = diff_df["iv_diff"].to_numpy()

    def _rmse(x):
        x = np.asarray(x, float); x = x[~np.isnan(x)]
        return float(np.sqrt(np.mean(x**2))) if x.size else float("nan")

    sc = {
        "n": int(len(diff_df)),
        "iv_rmse": _rmse(iv),
        "iv_mae": float(np.nanmean(np.abs(iv))),
        "iv_rmse_by_region": {b: _rmse(iv[bucket == b]) for b in ("lower", "atm", "upper")},
        "price_rmse": _rmse(diff_df["price_diff"]),
        "price_mae": float(np.nanmean(np.abs(diff_df["price_diff"]))),
        "price_mape": float(np.nanmean(np.abs(diff_df["price_diff_pct"]))),
        "roundtrip_max": float(np.nanmax(np.abs(
            diff_df["bsm_at_market"] - diff_df["market_price"]))),
        "method_max_abs": float(np.nanmax(np.abs(np.concatenate(
            [diff_df["crr_minus_bsm"], diff_df["tri_minus_bsm"]])))),
        "put_call_iv_gap": _put_call_iv_gap(diff_df),
    }
    return sc


def attach_broker(diff_df: pd.DataFrame, broker_iv, broker_greeks=None) -> pd.DataFrame:
    """Diff our inverted IV / Greeks against a broker's published values (Upstox path).

    ``broker_iv`` is a per-row array; ``broker_greeks`` an optional dict of per-row arrays
    keyed by Greek name. Adds ``*_broker`` and ``*_vs_broker`` columns. Requires the live
    Upstox chain (token), so it is never exercised by the offline tests.
    """
    out = diff_df.copy()
    out["iv_broker"] = np.asarray(broker_iv, float)
    out["iv_vs_broker"] = out["market_iv"] - out["iv_broker"]
    for gk, vals in (broker_greeks or {}).items():
        out[f"{gk}_broker"] = np.asarray(vals, float)
        out[f"{gk}_vs_broker"] = out[gk] - out[f"{gk}_broker"]
    return out


# --- house-style display (§8: 6 decimals, comma thousands, signed %) ---------------

def _num(x):
    return "nan" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:,.6f}"


def _pct(x):
    return "nan" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x * 100:+.6f}%"


def format_scorecard(sc: dict) -> str:
    """Render a :func:`scorecard` dict as an aligned, house-style text block."""
    by = sc["iv_rmse_by_region"]
    lines = [
        f"quotes                : {sc['n']:,}",
        f"IV RMSE (vs model)    : {_num(sc['iv_rmse'])}   (vol points)",
        f"IV MAE                : {_num(sc['iv_mae'])}",
        f"  lower / atm / upper : {_num(by['lower'])} / {_num(by['atm'])} / {_num(by['upper'])}",
        f"price RMSE            : {_num(sc['price_rmse'])}",
        f"price MAE             : {_num(sc['price_mae'])}",
        f"price MAPE            : {_pct(sc['price_mape'])}",
        f"inversion round-trip  : {_num(sc['roundtrip_max'])}   (max |BSM(IV)-mkt|)",
        f"BSM vs lattice max    : {_num(sc['method_max_abs'])}   (CRR & trinomial)",
        f"put-call IV gap max   : {_num(sc['put_call_iv_gap'])}",
    ]
    return "\n".join(lines)
