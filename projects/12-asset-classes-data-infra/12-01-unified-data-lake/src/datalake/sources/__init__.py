"""Swappable market-data sources (Upstox / NSE / yfinance) behind one protocol.

Public sources (yfinance, NSE bhavcopy) always register. The Upstox source is private
(gitignored) and registered only if present — so the public repo still imports cleanly.
"""
from .base import MarketData, available, get, register
from .nse_bhavcopy import NSEBhavcopySource
from .yfinance_source import YFinanceSource

register(YFinanceSource())
register(NSEBhavcopySource())

try:  # private module — absent in the public repo
    from .upstox_source import UpstoxSource
    register(UpstoxSource())
except Exception:  # noqa: BLE001
    pass

try:  # private module — absent in the public repo (reads the local Bullseye DB)
    from .bullseye_seed import BullseyeSeedSource
    register(BullseyeSeedSource())
except Exception:  # noqa: BLE001
    pass

__all__ = ["MarketData", "YFinanceSource", "NSEBhavcopySource",
           "register", "get", "available"]
