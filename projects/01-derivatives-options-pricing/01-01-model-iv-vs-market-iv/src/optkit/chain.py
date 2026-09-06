"""OptionChain — a strike × expiry grid of quotes, plus the fixtures that fill one.

An :class:`OptionChain` is the unit the surface layer consumes: parallel arrays of
``strike``, ``kind``, ``ttm`` (years), a per-row ``spot``/``r``/``q``, and whichever of
``market_price`` / ``market_iv`` the source gave us (the other is derived). Two ways to
get one:

* :func:`synthetic_smile_chain` — a deterministic, arbitrage-plausible smile priced with
  BSM. This is what the offline tests and the report's controlled experiments use (no
  network, no token, convention 11).
* :func:`OptionChain.from_fo_frame` — parse a real **NSE F&O bhavcopy** frame (the keyless
  EOD source in the data lake) into a chain, taking each option's settlement ``close`` as
  its market price. Market IV is then *inverted* downstream. This is the offline stand-in
  for the live Upstox chain, which needs a token this machine does not have.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

__all__ = ["OptionChain", "synthetic_smile_chain", "implied_spot_from_future"]


def _kinds(kind, n):
    """Broadcast a scalar/str/array ``kind`` to a length-``n`` lowercase array."""
    arr = np.array(np.broadcast_to(np.asarray(kind, dtype=object), (n,)), dtype=object)
    return np.array([str(k).lower() for k in arr], dtype=object)


@dataclass
class OptionChain:
    """A set of option quotes sharing nothing but a schema. All arrays share length ``n``.

    Exactly one of ``market_price`` / ``market_iv`` is required from a data source; the
    surface layer fills the other. ``spot``, ``r``, ``q`` may be scalars (broadcast) or
    per-row arrays — per-row lets one chain span several underlyings or as-of dates.
    """

    strike: np.ndarray
    kind: np.ndarray               # 'call'/'put' per row
    ttm: np.ndarray                # time to expiry, years
    spot: np.ndarray
    r: np.ndarray = None
    q: np.ndarray = None
    market_price: np.ndarray = None
    market_iv: np.ndarray = None
    label: np.ndarray = None       # free-form tag per row (e.g. expiry date)

    def __post_init__(self):
        self.strike = np.asarray(self.strike, dtype=float)
        n = self.strike.size
        self.kind = _kinds(self.kind, n)
        self.ttm = np.broadcast_to(np.asarray(self.ttm, dtype=float), (n,)).copy()
        self.spot = np.broadcast_to(np.asarray(self.spot, dtype=float), (n,)).copy()
        self.r = np.broadcast_to(np.asarray(0.0 if self.r is None else self.r, float), (n,)).copy()
        self.q = np.broadcast_to(np.asarray(0.0 if self.q is None else self.q, float), (n,)).copy()
        for name in ("market_price", "market_iv"):
            v = getattr(self, name)
            if v is not None:
                setattr(self, name, np.broadcast_to(np.asarray(v, float), (n,)).copy())
        if self.market_price is None and self.market_iv is None:
            raise ValueError("chain needs at least one of market_price / market_iv")
        if self.label is not None:
            self.label = np.asarray(self.label, dtype=object).reshape(-1)

    def __len__(self):
        return self.strike.size

    @property
    def forward(self):
        """Forward price ``F = S·e^{(r-q)t}`` per row."""
        return self.spot * np.exp((self.r - self.q) * self.ttm)

    @property
    def log_moneyness(self):
        """``k = ln(K / F)`` — 0 at-the-money-forward, <0 for ITM calls."""
        return np.log(self.strike / self.forward)

    def as_frame(self) -> pd.DataFrame:
        cols = {"strike": self.strike, "kind": self.kind, "ttm": self.ttm,
                "spot": self.spot, "r": self.r, "q": self.q,
                "forward": self.forward, "log_moneyness": self.log_moneyness}
        if self.market_price is not None:
            cols["market_price"] = self.market_price
        if self.market_iv is not None:
            cols["market_iv"] = self.market_iv
        if self.label is not None:
            cols["label"] = self.label
        return pd.DataFrame(cols)

    @classmethod
    def from_fo_frame(cls, df, spot, r=0.0, q=0.0, asof=None, day_count=365.0):
        """Build a chain from a canonical NSE **F&O bhavcopy** frame (data-lake schema).

        Parses option rows whose ``instrument_key`` is ``NSE_FO|SYM|EXPIRY|STRIKE|CE|PE``
        (futures / non-option rows are ignored) and takes ``close`` as the market price.
        ``asof`` defaults to each row's own ``ts`` date; TTM is ``(expiry - asof)/day_count``.
        """
        rows = []
        ts_col = pd.to_datetime(df["ts"]) if "ts" in df.columns else None
        for i, key in enumerate(df["instrument_key"].astype(str).to_numpy()):
            parts = key.split("|")
            if len(parts) != 5 or parts[0] != "NSE_FO" or parts[4] not in ("CE", "PE"):
                continue
            _, _sym, expiry, strike, cp = parts
            asof_i = pd.to_datetime(asof) if asof is not None else (
                ts_col.iloc[i] if ts_col is not None else None)
            ttm = (pd.to_datetime(expiry) - asof_i).days / day_count if asof_i is not None else np.nan
            rows.append((float(strike), "call" if cp == "CE" else "put",
                         ttm, float(df["close"].to_numpy()[i]), expiry))
        if not rows:
            raise ValueError("no NSE_FO option rows found in frame")
        strike, kind, ttm, price, label = zip(*rows)
        return cls(strike=np.array(strike), kind=np.array(kind, dtype=object),
                   ttm=np.array(ttm), spot=spot, r=r, q=q,
                   market_price=np.array(price), label=np.array(label, dtype=object))


def implied_spot_from_future(future_price, t, r, q=0.0):
    """Back out spot from a synchronous future: ``S = F·e^{-(r-q)t}``.

    For index options the same-expiry future is the cleaner forward reference than a
    laggy cash index, so we imply spot from it and price off a consistent carry.
    """
    return float(future_price) * np.exp(-(r - q) * t)


def synthetic_smile_chain(spot=100.0, r=0.05, q=0.0, ttms=(0.25,), strikes=None,
                          atm_vol=0.20, skew=-0.15, curv=0.60, kinds="both"):
    """A deterministic BSM-priced smile: ``σ(k) = atm_vol + skew·k + curv·k²`` (k = ln K/F).

    Returns a chain carrying **both** ``market_price`` and ``market_iv`` (the true smile),
    so tests can assert that inversion recovers the input IV exactly and that a flat-vol
    model reproduces the planted skew/curvature. Negative ``skew`` gives the equity-style
    downside smirk. ``kinds`` is ``"call"``, ``"put"``, or ``"both"`` (OTM side per strike).
    """
    from .bsm import bsm_price          # local import keeps chain.py import-light

    if strikes is None:
        strikes = np.round(spot * np.linspace(0.80, 1.20, 9), 2)
    strikes = np.asarray(strikes, dtype=float)

    S_all, K_all, t_all, cp_all, iv_all, lbl_all = [], [], [], [], [], []
    for t in ttms:
        F = spot * np.exp((r - q) * t)
        for K in strikes:
            k = np.log(K / F)
            iv = max(atm_vol + skew * k + curv * k * k, 0.01)
            if kinds == "both":
                cp = "call" if K >= F else "put"      # the liquid OTM wing
            else:
                cp = kinds
            S_all.append(spot); K_all.append(K); t_all.append(t)
            cp_all.append(cp); iv_all.append(iv); lbl_all.append(f"T={t:g}")
    iv_arr = np.array(iv_all)
    price = bsm_price(np.array(S_all), np.array(K_all), np.array(t_all),
                      r, iv_arr, q, np.array(cp_all, dtype=object))
    return OptionChain(strike=np.array(K_all), kind=np.array(cp_all, dtype=object),
                       ttm=np.array(t_all), spot=spot, r=r, q=q,
                       market_price=np.asarray(price), market_iv=iv_arr,
                       label=np.array(lbl_all, dtype=object))
