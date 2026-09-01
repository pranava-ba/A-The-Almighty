# 07-02 · Order-book imbalance & micro-price signal

From the depth feed, build OBI/micro-price features to predict short-horizon returns.

> Subproject **07-02** of section [07 · Market Microstructure & Execution](..). Part of the
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
`quant_lab/coverage.json`. Candidates from section 07:
  - [ ] Limit order book / matching engine
  - [ ] Transaction-cost / slippage modeling
  - [ ] Order flow / order imbalance
  - [ ] Market impact modeling
  - [ ] VWAP / execution benchmarks
  - [ ] Tick-level / odd-lot microstructure factors
  - [ ] Optimal execution (Almgren-Chriss)
  - [ ] Micro-price / OBI analytics
  - [ ] Closing-auction dynamics
  - [ ] ETF rebalancing / mechanics
  - [ ] Optimal execution as a Markov Decision Process
  - [ ] Regime-switching / stochastic liquidity
  - [ ] Information-based microstructure (Kyle, Glosten-Milgrom)

## Data
Sources (per portfolio rules): **Upstox** · **NSE bhavcopy** · **yfinance**, stored in the
DuckDB lake. **No data is committed** — reproduce via the free keyless sources.
