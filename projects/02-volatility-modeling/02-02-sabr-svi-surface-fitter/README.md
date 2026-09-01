# 02-02 · SABR / SVI surface fitter

Fit SABR and SVI to the NIFTY chain; classify low/high-vol regimes by VIX bands and study surface dynamics.

> Subproject **02-02** of section [02 · Volatility Modeling & Trading](..). Part of the
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
`quant_lab/coverage.json`. Candidates from section 02:
  - [ ] Volatility forecasting
  - [ ] Realized-vol estimators
  - [ ] Regime-switching volatility (DS3M / hybrid rough-regime)
  - [ ] Volatility surface / regime analysis
  - [ ] Heston stochastic-vol model
  - [ ] Rough volatility (rough Bergomi, Hurst, fBM)
  - [ ] SABR model
  - [ ] SVI surface
  - [ ] Jump-diffusion model
  - [ ] Implied-tail / higher-moment trading
  - [ ] Volatility / roughness risk premium
  - [ ] Short-volatility arbitrage

## Data
Sources (per portfolio rules): **Upstox** · **NSE bhavcopy** · **yfinance**, stored in the
DuckDB lake. **No data is committed** — reproduce via the free keyless sources.
