"""NSE bhavcopy adapter — free, keyless EOD equity candles (UDiFF CM format).

Downloads the daily UDiFF common-bhavcopy zip, unzips, and maps it to canonical candles.
EOD only (`interval='1day'`). The raw→canonical mapping (`_parse_cm`) is pure, so it is
tested offline; the live download is best-effort (NSE archives sometimes need a browser
session/cookie). F&O bhavcopy (with OI) is a planned extension.
"""
from __future__ import annotations

import pandas as pd

from ..schema import COLUMNS, canonical

_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
_CM = "https://nsearchives.nseindia.com/content/cm/BhavCopy_NSE_CM_0_0_0_{ymd}_F_0000.csv.zip"
_FO = "https://nsearchives.nseindia.com/content/fo/BhavCopy_NSE_FO_0_0_0_{ymd}_F_0000.csv.zip"


class NSEBhavcopySource:
    name = "nse_bhavcopy"

    def candles(self, instrument_key: str, interval: str = "1day",
                start=None, end=None) -> pd.DataFrame:
        if interval != "1day":
            raise ValueError("NSE bhavcopy is EOD only (interval='1day')")
        symbol = str(instrument_key).split("|")[-1]        # 'NSE_EQ|RELIANCE' or 'RELIANCE'
        frames = []
        for d in pd.bdate_range(start, end):               # skip weekends; holidays 404 → skipped
            try:
                frames.append(self._parse_cm(self.bhavcopy_cm(d.date()), symbol))
            except Exception:
                continue
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=COLUMNS)

    @staticmethod
    def _fetch_csv(url: str) -> pd.DataFrame:
        """Download + unzip a bhavcopy zip into a raw DataFrame."""
        import io
        import zipfile

        import requests
        r = requests.get(url, headers={"User-Agent": _UA, "Accept": "*/*"}, timeout=30)
        r.raise_for_status()
        z = zipfile.ZipFile(io.BytesIO(r.content))
        return pd.read_csv(z.open(z.namelist()[0]))

    @classmethod
    def bhavcopy_cm(cls, d) -> pd.DataFrame:
        """One day's UDiFF CM (cash-equity) bhavcopy, raw."""
        return cls._fetch_csv(_CM.format(ymd=pd.Timestamp(d).strftime("%Y%m%d")))

    @classmethod
    def bhavcopy_fo(cls, d) -> pd.DataFrame:
        """One day's UDiFF F&O bhavcopy (futures + options, with OI/settlement), raw."""
        return cls._fetch_csv(_FO.format(ymd=pd.Timestamp(d).strftime("%Y%m%d")))

    @staticmethod
    def _parse_cm(raw: pd.DataFrame, symbol: str | None = None) -> pd.DataFrame:
        df = raw
        if "FinInstrmTp" in df.columns:                    # keep cash-equity rows only
            df = df[df["FinInstrmTp"].astype(str).str.upper().isin(["STK", "EQ"])]
        if symbol is not None:
            df = df[df["TckrSymb"].astype(str) == symbol]
        if len(df) == 0:
            return pd.DataFrame(columns=COLUMNS)
        mapped = pd.DataFrame({
            "instrument_key": "NSE_EQ|" + df["TckrSymb"].astype(str).to_numpy(),
            "interval": "1day",
            "ts": pd.to_datetime(df["TradDt"]).to_numpy(),
            "open": df["OpnPric"].to_numpy(), "high": df["HghPric"].to_numpy(),
            "low": df["LwPric"].to_numpy(), "close": df["ClsPric"].to_numpy(),
            "volume": df["TtlTradgVol"].to_numpy(),
        })
        return canonical(mapped, "nse_bhavcopy")

    @staticmethod
    def _parse_fo(raw: pd.DataFrame, symbol: str | None = None) -> pd.DataFrame:
        """F&O bhavcopy → canonical, with OI. instrument_key encodes symbol|expiry|(strike|CE/PE)
        for options, symbol|expiry|FUT for futures."""
        df = raw
        if symbol is not None:
            df = df[df["TckrSymb"].astype(str) == symbol]
        if len(df) == 0:
            return pd.DataFrame(columns=COLUMNS)
        opt = (df["OptnTp"].astype(str).str.upper() if "OptnTp" in df.columns
               else pd.Series([""] * len(df), index=df.index))
        tk = df["TckrSymb"].astype(str).to_numpy()
        xp = df["XpryDt"].astype(str).to_numpy()
        sk = df["StrkPric"].astype(str).to_numpy() if "StrkPric" in df.columns else [""] * len(df)
        keys = [f"NSE_FO|{tk[i]}|{xp[i]}|{sk[i]}|{opt.iloc[i]}" if opt.iloc[i] in ("CE", "PE")
                else f"NSE_FO|{tk[i]}|{xp[i]}|FUT" for i in range(len(df))]
        mapped = pd.DataFrame({
            "instrument_key": keys, "interval": "1day",
            "ts": pd.to_datetime(df["TradDt"]).to_numpy(),
            "open": df["OpnPric"].to_numpy(), "high": df["HghPric"].to_numpy(),
            "low": df["LwPric"].to_numpy(), "close": df["ClsPric"].to_numpy(),
            "volume": df["TtlTradgVol"].to_numpy(), "oi": df["OpnIntrst"].to_numpy(),
        })
        return canonical(mapped, "nse_bhavcopy")
