# 14-01 · LOB simulator seeded by Upstox depth

Replay recorded depth + inject synthetic agents to test strategy fills under realistic microstructure.

> Subproject **14-01** of section [14 · Market Simulation & Agent-Based / Behavioral Finance](..). Part of the
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
`quant_lab/coverage.json`. Candidates from section 14:
  - [ ] Agent-based market simulation
  - [ ] Heterogeneous-investor / behavioral modeling
  - [ ] Market equilibrium / multi-agent incentive design
  - [ ] Limit order book / matching engine (simulated)
  - [ ] Stylized-facts calibration (fat tails, vol clustering)
  - [ ] Informed-trader / Kyle price discovery

## Data
Sources (per portfolio rules): **Upstox** · **NSE bhavcopy** · **yfinance**, stored in the
DuckDB lake. **No data is committed** — reproduce via the free keyless sources.
