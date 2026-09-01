# 12-01 · Unified data lake

Ingest instruments + candles across NSE_EQ/NSE_FO/MCX_FO/NSE_CD/BSE_EQ into Parquet/DuckDB with incremental updates.

> Subproject **12-01** of section [12 · Asset Classes & Data Infrastructure](..). Part of the
> Quant Portfolio — the durable contract is the root [`PORTFOLIO_SPEC.md`](../../../PORTFOLIO_SPEC.md).

## Definition of done
- [ ] `src/` — implementation (imports shared code from `quant_lab/common/`)
- [ ] `tests/` — pass offline with **synthetic fixtures**, no token / no network
- [ ] [`reading.md`](reading.md) — theory + derivations + harvested papers
- [ ] [`report.md`](report.md) — results via the shared tearsheet + honest caveats
- [ ] `demo/` — only if a live Streamlit genuinely helps
- [ ] concepts registered in `quant_lab/coverage.json` and actually exercised
- [ ] graph + coverage regenerated; docs updated; pushed green

## Concepts this subproject may cover
Tick the Table-A concepts this subproject *directly* implements, then register them in
`quant_lab/coverage.json`. Candidates from section 12:
  - [ ] Equities (single-stock & index)
  - [ ] FX / currencies
  - [ ] Commodities
  - [ ] Crypto / digital assets (via external feeds)
  - [ ] Prediction markets (external)
  - [ ] Real estate (external)
  - [ ] Point-in-time / survivorship-bias-free data
  - [ ] Corporate-action adjustment (splits, bonus, dividends)

## Data
Sources (per portfolio rules): **Upstox** · **NSE bhavcopy** · **yfinance**, stored in the
DuckDB lake. **No data is committed** — reproduce via the free keyless sources.
