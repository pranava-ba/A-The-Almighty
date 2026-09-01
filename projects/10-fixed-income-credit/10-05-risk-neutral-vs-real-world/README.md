# 10-05 · Risk-neutral vs real-world survival curves

Compare risk-neutral survival probabilities (from the JLT engine) against real-world estimates from rating-transition data across grades and horizons; decompose the risky forward rate into risk-free + credit terms.

> Subproject **10-05** of section [10 · Fixed Income & Credit](..). Part of the
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
`quant_lab/coverage.json`. Candidates from section 10:
  - [ ] Fixed income / bond analytics
  - [ ] Credit risk / default modeling
  - [ ] Credit stress testing
  - [ ] Option-Adjusted Spread (OAS)
  - [ ] Yield-curve / yield-data covariance
  - [ ] Insurance / loss modeling
  - [ ] Rating-transition credit model (Jarrow-Lando-Turnbull)
  - [ ] Risk-neutral survival / default probabilities
  - [ ] Defaultable-bond pricing & credit spreads
  - [ ] Options on defaultable bonds
  - [ ] Credit hedging (rate vs credit separation)
  - [ ] Short-rate / interest-rate models

## Data
Sources (per portfolio rules): **Upstox** · **NSE bhavcopy** · **yfinance**, stored in the
DuckDB lake. **No data is committed** — reproduce via the free keyless sources.
