# 14 · Market Simulation & Agent-Based / Behavioral Finance

Build a limit-order-book simulator seeded by real Upstox depth, populate it with heterogeneous agents, and study emergent stylized facts and multi-agent equilibria.

> Part of the **Quant Lab** — section 14 of 15. Derived from **Table A** of
> `RESUME_CONCEPT_TABLES.md`, cross-referencing **Table B** (math/stats) and
> **Table C** (technical). Data & execution via the **Upstox API**.

## Table A — Financial concepts (this section)
- Agent-based market simulation
- Heterogeneous-investor / behavioral modeling
- Market equilibrium / multi-agent incentive design
- Limit order book / matching engine (simulated)
- Stylized-facts calibration (fat tails, vol clustering)
- Informed-trader / Kyle price discovery

## Table B — Math & statistics (referenced)
- Stochastic processes / SDEs
- Markov models
- Dynamical systems / ergodic theory
- Monte Carlo simulation
- Game theory (equilibrium)
- Method of simulated moments / calibration
- Information asymmetry (Kyle, Glosten-Milgrom)

## Table C — Technical & computational (referenced)
- Python
- C++ (fast LOB simulator)
- Agent-based / multi-agent systems
- Concurrency / multithreading
- Backtesting-engine design

## Upstox data sources
| Source | What it gives you |
|---|---|
| `market_depth_ws` | Real-time 5-level order book + LTP via the market-data websocket feed. |
| `historical_candles` | OHLCV candles: 1minute/30minute/day/week/month over a date range. |
| `instruments_master` | Full tradable-instrument dump (all segments) with instrument_key symbology. |

Shared client: `from common import UpstoxClient` (set `UPSTOX_ACCESS_TOKEN`).

## Subprojects
| Folder | Project | What it does |
|---|---|---|
| [`14-01-lob-simulator-seeded-by-upstox`](14-01-lob-simulator-seeded-by-upstox) | **LOB simulator seeded by Upstox depth** | Replay recorded depth + inject synthetic agents to test strategy fills under realistic microstructure. |
| [`14-02-heterogeneous-agent-market`](14-02-heterogeneous-agent-market) | **Heterogeneous-agent market** | Momentum / value / noise traders with non-linear utilities; study wealth evolution and stylized facts. |
| [`14-03-multi-agent-equilibrium-incentive-design`](14-03-multi-agent-equilibrium-incentive-design) | **Multi-agent equilibrium / incentive design** | n-player market game with distributed equilibrium discovery. |
| [`14-04-stylized-facts-calibration-of-the`](14-04-stylized-facts-calibration-of-the) | **Stylized-facts calibration of the ABM** | Tune the agent mix (zero-intelligence vs momentum/value) via the method of simulated moments until the simulator reproduces fat tails, volatility clustering and the depth-imbalance/return relationship measured on real Upstox data. |
| [`14-05-kyle-informed-insider-agent`](14-05-kyle-informed-insider-agent) | **Kyle-informed insider agent** | Add a strategic informed trader (Kyle-style) to the LOB simulator and study how price discovery and market-maker losses scale with information asymmetry. |

## Research-paper bot
arXiv categories: `q-fin.TR`, `q-fin.CP`, `q-fin.EC`

Seed queries:
  - "agent based model financial market"
  - "limit order book simulation"
  - "heterogeneous agents market microstructure"

Run the bot for this section (writes `papers.md`):

```bash
python run_papers.py
```

## Interconnections
- **Depends on:** [Market Microstructure & Execution](../07-microstructure-execution), [Asset Classes & Data Infrastructure](../12-asset-classes-data-infra)
- **Feeds:** [Market Making](../06-market-making), [Systematic Trading Strategies](../04-systematic-trading), [Risk Management & Performance Metrics](../11-risk-performance)

See the full interconnected graph in [`../GRAPH.md`](../GRAPH.md) and
[`../graph.html`](../graph.html).
