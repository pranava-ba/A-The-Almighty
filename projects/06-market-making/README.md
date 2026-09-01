# 06 · Market Making

Quote two-sided around a fair-value micro-price with inventory-risk skewing; backtest against the real order book (Avellaneda-Stoikov and beyond).

> Part of the **Quant Lab** — section 06 of 15. Derived from **Table A** of
> `RESUME_CONCEPT_TABLES.md`, cross-referencing **Table B** (math/stats) and
> **Table C** (technical). Data & execution via the **Upstox API**.

## Table A — Financial concepts (this section)
- Market making (two-sided quoting)
- Inventory-risk management
- Fair-value mid / adaptive spreads
- Adverse selection (Glosten-Milgrom)
- Order-arrival intensity modelling (Hawkes)

## Table B — Math & statistics (referenced)
- Stochastic processes / SDEs (Avellaneda-Stoikov)
- Convex optimization
- Time-series analysis
- Markov models
- Dynamic programming / HJB (optimal quoting)
- Hawkes / self-exciting point processes

## Table C — Technical & computational (referenced)
- Python
- C++ (fast quoting loop)
- Low-latency / lock-free / SIMD / atomics
- Concurrency / multithreading
- Real-time dashboards / attribution
- Backtesting-engine design

## Upstox data sources
| Source | What it gives you |
|---|---|
| `market_depth_ws` | Real-time 5-level order book + LTP via the market-data websocket feed. |
| `market_quote_full` | Full quote: OHLC, depth snapshot, OI, volume, circuit limits. |
| `instruments_master` | Full tradable-instrument dump (all segments) with instrument_key symbology. |
| `orders_trades` | Order placement, modification, and trade book (execution). |

Shared client: `from common import UpstoxClient` (set `UPSTOX_ACCESS_TOKEN`).

## Subprojects
| Folder | Project | What it does |
|---|---|---|
| [`06-01-avellaneda-stoikov-mm-simulator`](06-01-avellaneda-stoikov-mm-simulator) | **Avellaneda-Stoikov MM simulator** | Quote around the micro-price with inventory skew; backtest fills against the recorded depth feed. |
| [`06-02-adverse-selection-study`](06-02-adverse-selection-study) | **Adverse-selection study** | Relate fill quality to order-flow imbalance to tune spread/skew. |
| [`06-03-inventory-aware-quote-sizing`](06-03-inventory-aware-quote-sizing) | **Inventory-aware quote sizing** | Optimize spread and skew as a function of inventory and volatility. |
| [`06-04-glosten-milgrom-adverse-selection-quoting`](06-04-glosten-milgrom-adverse-selection-quoting) | **Glosten-Milgrom adverse-selection quoting** | Set bid/ask from a sequential-trade information model; back out the information-driven spread component and compare it to realised adverse selection measured on the recorded depth feed. |
| [`06-05-hawkes-order-flow-modulated-quoting`](06-05-hawkes-order-flow-modulated-quoting) | **Hawkes order-flow-modulated quoting** | Fit a self-exciting Hawkes model to buy/sell order arrivals and use the estimated intensity to modulate quote aggressiveness and inventory skew. |

## Research-paper bot
arXiv categories: `q-fin.TR`, `q-fin.CP`, `q-fin.RM`

Seed queries:
  - "Avellaneda Stoikov market making"
  - "optimal market making inventory risk"
  - "reinforcement learning market making"

Run the bot for this section (writes `papers.md`):

```bash
python run_papers.py
```

## Interconnections
- **Depends on:** [Market Microstructure & Execution](../07-microstructure-execution), [Hedging & Greeks](../03-hedging-greeks), [Volatility Modeling & Trading](../02-volatility-modeling)
- **Feeds:** [Risk Management & Performance Metrics](../11-risk-performance)

See the full interconnected graph in [`../GRAPH.md`](../GRAPH.md) and
[`../graph.html`](../graph.html).
