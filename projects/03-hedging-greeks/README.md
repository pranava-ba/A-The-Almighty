# 03 · Hedging & Greeks

Simulate discrete delta/gamma hedging, decompose hedge P&L into vol-mispricing vs gamma, and build automated and tail-hedge overlays.

> Part of the **Quant Lab** — section 03 of 15. Derived from **Table A** of
> `RESUME_CONCEPT_TABLES.md`, cross-referencing **Table B** (math/stats) and
> **Table C** (technical). Data & execution via the **Upstox API**.

## Table A — Financial concepts (this section)
- Delta hedging
- Automated hedging strategies
- Gamma / hedge-error decomposition
- Tail hedging
- Multi-cash-flow hedging
- Full Greeks computation
- Deep / RL hedging

## Table B — Math & statistics (referenced)
- Stochastic processes / SDEs
- Brownian motion / Itô calculus
- Monte Carlo simulation
- Numerical methods / integration
- Time-series analysis

## Table C — Technical & computational (referenced)
- Python (NumPy/SciPy)
- Backtesting-engine design
- Real-time dashboards / attribution analytics
- Reinforcement learning (deep hedging)

## Upstox data sources
| Source | What it gives you |
|---|---|
| `option_chain` | Option chain by underlying+expiry with per-strike IV, greeks (Δ Γ Θ ν ρ), OI, LTP. |
| `historical_candles` | OHLCV candles: 1minute/30minute/day/week/month over a date range. |
| `market_depth_ws` | Real-time 5-level order book + LTP via the market-data websocket feed. |
| `portfolio_positions` | Intraday/derivative open positions and live P&L. |

Shared client: `from common import UpstoxClient` (set `UPSTOX_ACCESS_TOKEN`).

## Subprojects
| Folder | Project | What it does |
|---|---|---|
| [`03-01-discrete-delta-hedge-simulator`](03-01-discrete-delta-hedge-simulator) | **Discrete delta-hedge simulator** | Hedge a NIFTY option daily/intraday using chain greeks; decompose realized P&L into volatility-mispricing vs gamma components. |
| [`03-02-hedge-effectiveness-grid`](03-02-hedge-effectiveness-grid) | **Hedge-effectiveness grid** | Evaluate delta-hedge slippage across moneyness (0.7-1.3) and maturities using the option chain. |
| [`03-03-tail-hedge-overlay`](03-03-tail-hedge-overlay) | **Tail-hedge overlay** | Overlay OTM puts on an equity book; measure cost vs drawdown protection in stress windows. |
| [`03-04-deep-hedging-vs-delta-hedging`](03-04-deep-hedging-vs-delta-hedging) | **Deep hedging vs delta hedging (RL)** | Train an RL / deep-hedging agent to hedge a NIFTY option under transaction costs and discrete rebalancing; compare the terminal-P&L distribution and CVaR against Black-Scholes delta hedging. |

## Research-paper bot
arXiv categories: `q-fin.RM`, `q-fin.PR`, `q-fin.CP`

Seed queries:
  - "delta hedging discrete gamma error"
  - "deep hedging reinforcement learning"
  - "option hedging transaction costs"

Run the bot for this section (writes `papers.md`):

```bash
python run_papers.py
```

## Interconnections
- **Depends on:** [Derivatives & Options Pricing](../01-derivatives-options-pricing), [Volatility Modeling & Trading](../02-volatility-modeling)
- **Feeds:** [Market Making](../06-market-making), [Risk Management & Performance Metrics](../11-risk-performance)

See the full interconnected graph in [`../GRAPH.md`](../GRAPH.md) and
[`../graph.html`](../graph.html).
