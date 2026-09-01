# 01-04 · Finite-difference BS-PDE pricer + variance reduction

Price European and barrier options with explicit & implicit finite-difference BS-PDE solvers and a Monte-Carlo engine using antithetic / control-variate / importance sampling; study stability, convergence, and pricing error vs the Upstox chain.

> Subproject **01-04** of section [01 · Derivatives & Options Pricing](..). Part of the
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
`quant_lab/coverage.json`. Candidates from section 01:
  - [ ] Black-Scholes-Merton pricing
  - [ ] Monte Carlo pricing
  - [ ] Implied-volatility solving
  - [ ] Full Greeks computation
  - [ ] American options (LSMC)
  - [ ] Binomial (CRR) trees
  - [ ] Trinomial trees
  - [ ] Structured products (knock-in/out)
  - [ ] Gamma-Vanna-Volga model
  - [ ] Risk-neutral density extraction
  - [ ] Barrier / path-dependent options
  - [ ] Short-rate / interest-rate models

## Data
Sources (per portfolio rules): **Upstox** · **NSE bhavcopy** · **yfinance**, stored in the
DuckDB lake. **No data is committed** — reproduce via the free keyless sources.
