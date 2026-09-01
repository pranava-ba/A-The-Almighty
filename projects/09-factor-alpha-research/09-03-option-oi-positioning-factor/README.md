# 09-03 · Option-OI positioning factor

Derive a positioning/flow factor from the option chain OI and test it.

> Subproject **09-03** of section [09 · Factor / Alpha Research](..). Part of the
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
`quant_lab/coverage.json`. Candidates from section 09:
  - [ ] Alpha signal generation
  - [ ] Multi-factor models
  - [ ] Sentiment factor (news NLP)
  - [ ] Information Coefficient (IC / RankIC)
  - [ ] Return-direction prediction
  - [ ] Factor neutralization / style exposure
  - [ ] Barra risk model (CNE6)
  - [ ] Turnover / self-correlation control
  - [ ] Nowcasting (mixed-frequency)
  - [ ] Fama-MacBeth priced-factor testing
  - [ ] Backtest-overfitting control (deflated Sharpe, PBO)

## Data
Sources (per portfolio rules): **Upstox** · **NSE bhavcopy** · **yfinance**, stored in the
DuckDB lake. **No data is committed** — reproduce via the free keyless sources.
