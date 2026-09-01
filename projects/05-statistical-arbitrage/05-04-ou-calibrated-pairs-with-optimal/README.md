# 05-04 · OU-calibrated pairs with optimal bands

Model each spread as an Ornstein-Uhlenbeck process; estimate the half-life and derive entry/exit thresholds that maximise expected return per unit time (first-passage), then walk-forward with borrow and slippage costs.

> Subproject **05-04** of section [05 · Statistical Arbitrage & Relative Value](..). Part of the
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
`quant_lab/coverage.json`. Candidates from section 05:
  - [ ] Statistical arbitrage / pairs trading
  - [ ] Cointegration trading (Engle-Granger, ADF)
  - [ ] Relative-value trading
  - [ ] Commodity spread trading
  - [ ] Risk-free / triangular arbitrage
  - [ ] Ornstein-Uhlenbeck spread trading (optimal bands)
  - [ ] Kalman dynamic hedge ratio

## Data
Sources (per portfolio rules): **Upstox** · **NSE bhavcopy** · **yfinance**, stored in the
DuckDB lake. **No data is committed** — reproduce via the free keyless sources.
