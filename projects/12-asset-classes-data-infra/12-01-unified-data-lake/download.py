"""Rebuild the local DuckDB lake from the FREE, keyless sources — no Upstox token needed.

This is what makes the repo reproducible by a stranger: no data is shipped, but anyone can
run this to pull a starter universe from yfinance (and, optionally, NSE bhavcopy) into a
local DuckDB. Idempotent — safe to re-run to extend history.

  python download.py                                   # default watchlist, daily, to a local db
  python download.py --db lake.duckdb --start 2024-01-01 --end 2026-08-28
  python download.py --tickers "^NSEI,^NSEBANK,RELIANCE.NS" --interval 1day
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from datalake import DuckDBStore, backfill  # noqa: E402
from datalake.sources import YFinanceSource  # noqa: E402

# A small, illustrative default universe (Yahoo tickers): the big NSE indices, India VIX,
# a couple of ETFs, and a few large caps. Extend freely — nothing here is committed.
DEFAULT = [
    "^NSEI", "^NSEBANK", "^CNXIT", "^BSESN", "^INDIAVIX",
    "NIFTYBEES.NS", "BANKBEES.NS",
    "RELIANCE.NS", "HDFCBANK.NS", "TCS.NS", "INFY.NS", "ICICIBANK.NS",
]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default="lake.duckdb", help="DuckDB path (created if absent)")
    ap.add_argument("--tickers", default=",".join(DEFAULT), help="comma-separated Yahoo tickers")
    ap.add_argument("--interval", default="1day")
    ap.add_argument("--start", default="2024-01-01")
    ap.add_argument("--end", default=None)
    a = ap.parse_args(argv)

    store = DuckDBStore(a.db)
    src = YFinanceSource()
    total = 0
    for t in [x.strip() for x in a.tickers.split(",") if x.strip()]:
        try:
            n = backfill(store, src, t, a.interval, start=a.start, end=a.end)
            total += n
            print(f"  {t:16} {n:>6} bars")
        except Exception as e:  # noqa: BLE001
            print(f"  {t:16} FAILED: {type(e).__name__} {str(e)[:80]}")
    print(f"lake: {a.db}  |  {store.count()} rows total  (+{total} this run)")
    store.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
