# 15-04 · Generative scenarios for risk (GAN / diffusion)

Train a GAN/diffusion model on index-return histories to generate synthetic stress scenarios for VaR/ES and portfolio stress-testing (11), validated against historical crises.

> Subproject **15-04** of section [15 · Machine Learning & Alternative Data](..). Part of the
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
`quant_lab/coverage.json`. Candidates from section 15:
  - [ ] Sentiment factor (news NLP)
  - [ ] Alpha signal generation
  - [ ] Return-direction prediction
  - [ ] Nowcasting (mixed-frequency)
  - [ ] Cross-asset / regime-switching allocation (ML regime)
  - [ ] Stress testing / scenario analysis (ML)

## Data
Sources (per portfolio rules): **Upstox** · **NSE bhavcopy** · **yfinance**, stored in the
DuckDB lake. **No data is committed** — reproduce via the free keyless sources.
