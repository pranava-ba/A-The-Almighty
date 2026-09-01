"""Cross-source reconciliation + gap-fill (subproject 12-05).

Given the SAME instrument/interval fetched from several sources, `reconcile`:
  - drops **bad prints** (high<low, non-positive, o/c outside [low,high]),
  - counts **cross-source mismatches** (close prices that disagree beyond a tolerance),
  - **gap-fills** into one merged series (primary source, holes filled from the others),
  - returns a per-instrument **data-quality scorecard**.
This is what lets us trust a candle that came from a free/unofficial feed.
"""
from __future__ import annotations

import pandas as pd

from .schema import COLUMNS


def bad_print_mask(df: pd.DataFrame) -> pd.Series:
    """True where a candle is internally inconsistent or non-positive."""
    o, h, l, c = (pd.to_numeric(df[x], errors="coerce") for x in ("open", "high", "low", "close"))
    bad = (h < l) | (l <= 0) | (o <= 0) | (c <= 0) | (h < o) | (h < c) | (l > o) | (l > c)
    return bad.fillna(True)


def reconcile(frames: dict[str, pd.DataFrame], primary: str | None = None,
              price_tol: float = 0.005, expected_ts=None) -> tuple[pd.DataFrame, dict]:
    """`frames`: {source_name -> canonical candles} for one instrument+interval.
    Returns (merged canonical frame, scorecard)."""
    names = list(frames)
    if not names:
        return pd.DataFrame(columns=COLUMNS), {"sources": {}, "merged_rows": 0}
    primary = primary if primary in frames else names[0]

    cleaned, report = {}, {}
    for name, df in frames.items():
        bad = bad_print_mask(df)
        report[name] = {"rows": int(len(df)), "bad_prints": int(bad.sum())}
        cleaned[name] = df[~bad].drop_duplicates("ts").set_index("ts")

    union = set().union(*[set(d.index) for d in cleaned.values()])

    mism = compared = 0
    p = cleaned[primary]
    for name, d in cleaned.items():
        if name == primary:
            continue
        shared = p.index.intersection(d.index)
        compared += len(shared)
        if len(shared):
            pc = pd.to_numeric(p.loc[shared, "close"], errors="coerce").abs()
            dc = pd.to_numeric(d.loc[shared, "close"], errors="coerce")
            rel = (pc - dc).abs() / pc.replace(0, pd.NA)
            mism += int((rel > price_tol).sum())

    merged = p.copy()
    for name in names:
        if name == primary:
            continue
        missing = cleaned[name].index.difference(merged.index)
        if len(missing):
            merged = pd.concat([merged, cleaned[name].loc[missing]])
    merged = merged.sort_index().reset_index()[COLUMNS]

    scorecard = {
        "primary": primary,
        "sources": report,
        "union_ts": len(union),
        "merged_rows": int(len(merged)),
        "cross_source_mismatches": mism,
        "compared_overlap": compared,
        "coverage": {n: round(len(cleaned[n]) / len(union), 4) if union else 0.0 for n in names},
    }
    if expected_ts is not None:
        exp = set(pd.to_datetime(pd.Series(list(expected_ts))))
        scorecard["missing_vs_expected"] = int(len(exp - set(merged["ts"])))
    return merged, scorecard
