# 03-01 · Discrete delta-hedge simulator

Hedge a NIFTY option daily/intraday using chain greeks; decompose realized P&L into volatility-mispricing vs gamma components.

> Subproject **03-01** of section [03 · Hedging & Greeks](..). Part of the
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
`quant_lab/coverage.json`. Candidates from section 03:
  - [ ] Delta hedging
  - [ ] Automated hedging strategies
  - [ ] Gamma / hedge-error decomposition
  - [ ] Tail hedging
  - [ ] Multi-cash-flow hedging
  - [ ] Full Greeks computation
  - [ ] Deep / RL hedging

## Data
Sources (per portfolio rules): **Upstox** · **NSE bhavcopy** · **yfinance**, stored in the
DuckDB lake. **No data is committed** — reproduce via the free keyless sources.
