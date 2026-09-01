# 08-01 · Nifty-50 MVO with shrinkage + constraints

cvxpy MVO with Ledoit-Wolf shrinkage, sector caps and no-short; trace the efficient frontier.

> Subproject **08-01** of section [08 · Portfolio Construction & Optimization](..). Part of the
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
`quant_lab/coverage.json`. Candidates from section 08:
  - [ ] Mean-variance / Markowitz optimization
  - [ ] Efficient frontier
  - [ ] Portfolio constraints (sector caps, no-short, neutrality)
  - [ ] Dynamic rebalancing
  - [ ] Position / bet sizing
  - [ ] Stress testing / scenario analysis
  - [ ] Convex optimization for portfolios (cvxpy/MOSEK)
  - [ ] Regime / clustering-based construction
  - [ ] Beta-neutral / minimum-risk portfolio
  - [ ] Covariance / correlation shrinkage
  - [ ] Black-Litterman (views + equilibrium)
  - [ ] Hierarchical Risk Parity (HRP)
  - [ ] Mean-CVaR / tail-risk optimization

## Data
Sources (per portfolio rules): **Upstox** · **NSE bhavcopy** · **yfinance**, stored in the
DuckDB lake. **No data is committed** — reproduce via the free keyless sources.
