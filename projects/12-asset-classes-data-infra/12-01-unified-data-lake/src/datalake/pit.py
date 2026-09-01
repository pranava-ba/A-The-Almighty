"""Point-in-time universe + corporate-action adjustment (subproject 12-04).

Two leakage traps this closes:
  - **Survivorship bias:** query index membership *as of* a historical date, so a backtest
    only ever sees the names that were actually in the index then.
  - **Corporate actions:** back-adjust OHLC for splits/bonuses/dividends so a continuous
    series has no artificial jump at an ex-date.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


class PointInTimeUniverse:
    """Membership intervals `[start, end)` (end NaT/None = still a member). Query as-of a date."""

    def __init__(self, membership: pd.DataFrame):
        m = membership.copy()
        m["start"] = pd.to_datetime(m["start"])
        m["end"] = pd.to_datetime(m["end"])
        self.m = m

    def members_asof(self, index: str, date) -> list[str]:
        d = pd.to_datetime(date)
        m = self.m
        sel = m[(m["index"] == index) & (m["start"] <= d) & (m["end"].isna() | (m["end"] > d))]
        return sorted(sel["symbol"].tolist())


def adjust_candles(df: pd.DataFrame, actions: pd.DataFrame,
                   price_cols=("open", "high", "low", "close")) -> pd.DataFrame:
    """Back-adjust prices for corporate actions. `actions` has `ex_date` and `factor`, the
    multiplier applied to every bar STRICTLY BEFORE that ex-date (1:2 split → 0.5; bonus 1:1
    → 0.5; cash dividend → 1 − div/prev_close). A bar's total factor is the product of the
    factors of all actions dated after it — so old bars line up with today's price scale."""
    out = df.copy().sort_values("ts").reset_index(drop=True)
    tsv = pd.to_datetime(out["ts"]).to_numpy()
    factor = np.ones(len(out))
    a = actions.copy()
    a["ex_date"] = pd.to_datetime(a["ex_date"])
    for _, row in a.iterrows():
        factor[tsv < np.datetime64(row["ex_date"])] *= float(row["factor"])
    for c in price_cols:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce").to_numpy() * factor
    return out
