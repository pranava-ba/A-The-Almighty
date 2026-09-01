# Quant Portfolio

A single interconnected body of work in quantitative finance on Indian markets (NSE/BSE):
**72 subprojects** across 15 topic sections — options pricing, volatility, hedging,
systematic strategies, statistical arbitrage, market-making, microstructure, portfolio
optimization, factors, fixed income, risk, data infrastructure, valuation, market
simulation, and machine learning — all sitting on one **shared data layer** and reporting
through one **shared evaluation backbone**.

The organizing idea: *nothing is judged on a good-looking number.* Every result is
net-of-cost, point-in-time correct, survivorship-bias-free, and discounted for how many
things were tried before it looked good.

:::{admonition} New to quant finance? Start with the foundations.
:class: tip
The {doc}`foundations/index` track explains the ideas — returns, Sharpe, overfitting —
from zero, with no assumed background, before any of the technical pages.
:::

## What's here

- **{doc}`foundations/index`** — the domain from scratch: what a backtest is, how return and
  risk are measured, and why a great backtest is usually a lie.
- **{doc}`data_foundation`** — the unified DuckDB data lake: one schema, four swappable
  sources (Upstox, NSE bhavcopy, yfinance, and a local seed), cross-source reconciliation,
  point-in-time membership, and corporate-action adjustment.
- **{doc}`evaluation`** — the shared tearsheet: net-of-cost return, Sharpe, **deflated
  Sharpe**, drawdown, turnover, and leakage-aware cross-validation.
- **{doc}`concepts`** — the full concept map (financial, mathematical, and technical) the
  portfolio is built to cover.
- **{doc}`graph`** — the interactive interconnection graph of the whole lab.
- **{doc}`glossary`** — every term, defined once.
- **{doc}`progress`** — the dated build log.

```{toctree}
:hidden:
:caption: Start here
foundations/index
```

```{toctree}
:hidden:
:caption: The shared machinery
data_foundation
evaluation
```

```{toctree}
:hidden:
:caption: The map
concepts
graph
glossary
progress
```
