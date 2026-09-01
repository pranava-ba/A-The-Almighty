# 13-02 · DCF + Monte-Carlo scenario valuation

Probabilistic DCF with sensitivity/tornado analysis and IRR.

> Subproject **13-02** of section [13 · Corporate Finance & Valuation (IB/PE)](..). Part of the
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
`quant_lab/coverage.json`. Candidates from section 13:
  - [ ] DCF valuation
  - [ ] Due diligence / investment screening
  - [ ] Financial-statement / P&L analysis
  - [ ] Trading comparables (comps)
  - [ ] M&A analysis
  - [ ] LBO modeling
  - [ ] IRR / equity multiple / cash-on-cash
  - [ ] Real-estate underwriting
  - [ ] Market sizing / demand forecasting
  - [ ] Reverse-DCF / market-implied expectations
  - [ ] Real-options valuation (binomial/BSM on projects)

## Data
Sources (per portfolio rules): **Upstox** · **NSE bhavcopy** · **yfinance**, stored in the
DuckDB lake. **No data is committed** — reproduce via the free keyless sources.
