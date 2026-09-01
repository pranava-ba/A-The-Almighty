# 04-04 · Cross-market jump contagion (US/SGX → Nifty)

Test overnight transmission from US/SGX moves into the next-day Nifty open using a predetermined-regressor design off the time-zone gap; White-robust OLS + full diagnostics, 2SLS endogeneity check, bivariate VAR/Granger, jump detection, and crisis-interaction regressions separating contagion from interdependence (Forbes-Rigobon).

> Subproject **04-04** of section [04 · Systematic Trading Strategies](..). Part of the
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
`quant_lab/coverage.json`. Candidates from section 04:
  - [ ] Momentum / trend-following
  - [ ] Mean-reversion
  - [ ] Technical indicators (SMA, Bollinger, rolling averages)
  - [ ] Cross-asset / regime-switching allocation
  - [ ] Long/short equity (market-neutral)
  - [ ] Breakout strategy
  - [ ] Macro / event-driven trading
  - [ ] Post-earnings drift
  - [ ] Financial contagion / cross-market transmission

## Data
Sources (per portfolio rules): **Upstox** · **NSE bhavcopy** · **yfinance**, stored in the
DuckDB lake. **No data is committed** — reproduce via the free keyless sources.
