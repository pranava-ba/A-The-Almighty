"""DuckDB-backed store for the unified data lake — idempotent candle upsert + reads.

DuckDB (not loose Parquet/CSV) is the store of record for every pull, per the portfolio
data rule. `:memory:` for tests; a file path for the real lake (never committed).
"""
from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd

from .schema import COLUMNS, DDL


class DuckDBStore:
    def __init__(self, path: str | Path = ":memory:"):
        self.con = duckdb.connect(str(path))
        self.con.execute(DDL)

    def upsert_candles(self, df: pd.DataFrame) -> int:
        """Insert candles, updating on (instrument_key, interval, ts) conflicts — so a
        re-pull of an overlapping window never duplicates rows (idempotent backfill)."""
        if df.empty:
            return 0
        self.con.register("_incoming", df[COLUMNS])
        self.con.execute(
            "INSERT INTO candles SELECT * FROM _incoming "
            "ON CONFLICT (instrument_key, interval, ts) DO UPDATE SET "
            "open=excluded.open, high=excluded.high, low=excluded.low, close=excluded.close, "
            "volume=excluded.volume, oi=excluded.oi, source=excluded.source"
        )
        self.con.unregister("_incoming")
        return len(df)

    def read_candles(self, instrument_key: str, interval: str,
                     start=None, end=None) -> pd.DataFrame:
        q = "SELECT * FROM candles WHERE instrument_key=? AND interval=?"
        params: list = [instrument_key, interval]
        if start is not None:
            q += " AND ts>=?"; params.append(start)
        if end is not None:
            q += " AND ts<=?"; params.append(end)
        q += " ORDER BY ts"
        return self.con.execute(q, params).df()

    def count(self) -> int:
        return self.con.execute("SELECT count(*) FROM candles").fetchone()[0]

    def close(self) -> None:
        self.con.close()
