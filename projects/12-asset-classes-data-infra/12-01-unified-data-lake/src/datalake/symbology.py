"""Symbology normalizer (subproject 12-03).

One canonical identity per instrument across the sources: NSE trading symbol ↔ Upstox
`instrument_key` ↔ ISIN ↔ Yahoo ticker. Built from the (keyless) Upstox instrument master;
`from_upstox_master()` fetches it, or inject a list of instrument dicts for tests.
"""
from __future__ import annotations

import gzip
import json

_MASTER_URL = "https://assets.upstox.com/market-quote/instruments/exchange/complete.json.gz"

# Index symbols Yahoo names them differently from their exchange symbol.
_YAHOO_INDEX = {
    "NIFTY 50": "^NSEI", "NIFTY BANK": "^NSEBANK", "NIFTY FIN SERVICE": "^CNXFIN",
    "NIFTY IT": "^CNXIT", "INDIA VIX": "^INDIAVIX", "SENSEX": "^BSESN", "BANKEX": "^BSEBANK",
}


def fetch_upstox_master(segment: str | None = None) -> list[dict]:
    """The full Upstox instrument master (no auth). Optionally filter by `segment`."""
    import requests
    raw = requests.get(_MASTER_URL, timeout=60).content
    data = json.loads(gzip.decompress(raw))
    return [i for i in data if i.get("segment") == segment] if segment else data


class Symbology:
    def __init__(self, instruments: list[dict]):
        self._by_symbol: dict[tuple[str, str], dict] = {}
        self._by_isin: dict[str, dict] = {}
        for i in instruments:
            seg, sym, isin = i.get("segment"), i.get("trading_symbol"), i.get("isin")
            if seg and sym:
                self._by_symbol[(seg, sym)] = i
            if isin:
                self._by_isin.setdefault(isin, i)

    @classmethod
    def from_upstox_master(cls, segments=("NSE_EQ", "NSE_INDEX", "BSE_EQ", "BSE_INDEX")) -> "Symbology":
        data = fetch_upstox_master()
        if segments:
            data = [i for i in data if i.get("segment") in set(segments)]
        return cls(data)

    def upstox_key(self, symbol: str, segment: str = "NSE_EQ") -> str | None:
        i = self._by_symbol.get((segment, symbol))
        return i.get("instrument_key") if i else None

    def isin(self, symbol: str, segment: str = "NSE_EQ") -> str | None:
        i = self._by_symbol.get((segment, symbol))
        return i.get("isin") if i else None

    def by_isin(self, isin: str) -> dict | None:
        return self._by_isin.get(isin)

    def symbol_of_isin(self, isin: str) -> str | None:
        i = self._by_isin.get(isin)
        return i.get("trading_symbol") if i else None

    @staticmethod
    def yahoo(symbol: str, segment: str = "NSE_EQ") -> str:
        """Yahoo ticker for a symbol: indices via a lookup, else `.NS`/`.BO` suffix."""
        if symbol.upper() in _YAHOO_INDEX:
            return _YAHOO_INDEX[symbol.upper()]
        if segment.startswith("BSE"):
            return symbol + ".BO"
        return symbol + ".NS"
