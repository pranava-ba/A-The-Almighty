"""yfinance adapter — free, keyless index/ETF/stock candles (EOD + shallow intraday).

The instrument_key here is the Yahoo ticker (e.g. `^NSEI`, `RELIANCE.NS`); canonical
symbology mapping is subproject 12-03. The raw→canonical mapping (`_to_candles`) is a pure
function, so it's tested offline without hitting the network.
"""
from __future__ import annotations

import pandas as pd

from ..schema import COLUMNS, normalize

_INTERVAL = {"1minute": "1m", "5minute": "5m", "15minute": "15m", "30minute": "30m",
             "1hour": "1h", "1day": "1d", "1week": "1wk", "1month": "1mo"}


class YFinanceSource:
    name = "yfinance"

    def candles(self, instrument_key: str, interval: str = "1day",
                start=None, end=None) -> pd.DataFrame:
        import yfinance as yf  # imported lazily so the module loads without the dep
        yiv = _INTERVAL.get(interval, interval)
        raw = yf.download(instrument_key, interval=yiv, start=start, end=end,
                          auto_adjust=False, progress=False)
        return self._to_candles(raw, instrument_key, interval)

    @staticmethod
    def _to_candles(raw: pd.DataFrame, instrument_key: str, interval: str) -> pd.DataFrame:
        if raw is None or len(raw) == 0:
            return pd.DataFrame(columns=COLUMNS)
        df = raw.copy()
        if isinstance(df.columns, pd.MultiIndex):          # yfinance multi-ticker frames
            df.columns = df.columns.get_level_values(0)
        df = df.reset_index()
        tcol = df.columns[0]                                # 'Date' or 'Datetime'
        mapped = pd.DataFrame({
            "ts": df[tcol],
            "open": df["Open"], "high": df["High"], "low": df["Low"],
            "close": df["Close"], "volume": df["Volume"],
        })
        return normalize(mapped, instrument_key, interval, "yfinance")
