# 11-02 · VaR / Expected-Shortfall engine

Historical + Monte-Carlo VaR/ES on a live book.

> Subproject **11-02** of section [11 · Risk Management & Performance Metrics](..). Part of the
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
`quant_lab/coverage.json`. Candidates from section 11:
  - [ ] Systematic strategy backtesting
  - [ ] Sharpe ratio
  - [ ] Maximum drawdown
  - [ ] P&L attribution
  - [ ] Walk-forward / out-of-sample validation
  - [ ] Risk-adjusted return / alpha vs benchmark
  - [ ] Value at Risk (VaR)
  - [ ] Deflated Sharpe ratio
  - [ ] Fill ratio / spread capture
  - [ ] Hit rate / win rate
  - [ ] Protection rate (defensive)
  - [ ] Extreme-value-theory VaR/ES (POT/GPD)
  - [ ] Expected-shortfall backtesting (Acerbi-Szekely)
  - [ ] Copula tail-dependence

## Data
Sources (per portfolio rules): **Upstox** · **NSE bhavcopy** · **yfinance**, stored in the
DuckDB lake. **No data is committed** — reproduce via the free keyless sources.
