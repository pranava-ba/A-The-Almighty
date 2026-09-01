# 01 · Derivatives & Options Pricing

Price vanilla and exotic options with closed-form, lattice, and Monte-Carlo methods; recover implied vol and Greeks; benchmark model output against the live Upstox option chain.

> Part of the **Quant Lab** — section 01 of 15. Derived from **Table A** of
> `RESUME_CONCEPT_TABLES.md`, cross-referencing **Table B** (math/stats) and
> **Table C** (technical). Data & execution via the **Upstox API**.

## Table A — Financial concepts (this section)
- Black-Scholes-Merton pricing
- Monte Carlo pricing
- Implied-volatility solving
- Full Greeks computation
- American options (LSMC)
- Binomial (CRR) trees
- Trinomial trees
- Structured products (knock-in/out)
- Gamma-Vanna-Volga model
- Risk-neutral density extraction
- Barrier / path-dependent options
- Short-rate / interest-rate models

## Table B — Math & statistics (referenced)
- Stochastic processes / SDEs
- Brownian motion / Itô calculus
- Monte Carlo simulation
- Numerical methods / integration (Newton-Raphson, bisection)
- Differential equations / PDEs
- Linear algebra / matrix decompositions (Cholesky)
- Change of measure (Girsanov) & Feynman-Kac
- Numerical SDE/PDE & variance-reduction methods (Euler-Maruyama, Milstein, finite differences)

## Table C — Technical & computational (referenced)
- Python (NumPy/SciPy)
- C++ (fast pricers)
- Backtesting-engine design
- LaTeX / reproducible reporting

## Upstox data sources
| Source | What it gives you |
|---|---|
| `option_chain` | Option chain by underlying+expiry with per-strike IV, greeks (Δ Γ Θ ν ρ), OI, LTP. |
| `historical_candles` | OHLCV candles: 1minute/30minute/day/week/month over a date range. |
| `market_quote_full` | Full quote: OHLC, depth snapshot, OI, volume, circuit limits. |

Shared client: `from common import UpstoxClient` (set `UPSTOX_ACCESS_TOKEN`).

## Subprojects
| Folder | Project | What it does |
|---|---|---|
| [`01-01-model-iv-vs-market-iv`](01-01-model-iv-vs-market-iv) | **Model-IV vs market-IV surface** | Pull the NIFTY/BANKNIFTY option chain, compute BSM / CRR / trinomial prices and invert for IV, then diff against Upstox chain IV and greeks. |
| [`01-02-american-vs-european-premium`](01-02-american-vs-european-premium) | **American vs European premium** | LSMC (Longstaff-Schwartz) pricer on stock options; quantify the early-exercise premium vs a European CRR baseline. |
| [`01-03-structured-payoff-monte-carlo-pricer`](01-03-structured-payoff-monte-carlo-pricer) | **Structured-payoff Monte Carlo pricer** | Price knock-in/knock-out (SharkFin-style) payoffs on NIFTY via Monte Carlo, calibrated to the chain-implied surface. |
| [`01-04-finite-difference-bs-pde-pricer`](01-04-finite-difference-bs-pde-pricer) | **Finite-difference BS-PDE pricer + variance reduction** | Price European and barrier options with explicit & implicit finite-difference BS-PDE solvers and a Monte-Carlo engine using antithetic / control-variate / importance sampling; study stability, convergence, and pricing error vs the Upstox chain. |
| [`01-05-risk-neutral-valuation-from-first`](01-05-risk-neutral-valuation-from-first) | **Risk-neutral valuation from first principles** | Reproduce risk-neutral pricing binomial→continuous (replication, martingale measure, Girsanov, Feynman-Kac ↔ heat equation) and price barrier / path-dependent NIFTY claims, reconciling tree, PDE and MC — a derive-don't-cite reference implementation. |

## Research-paper bot
arXiv categories: `q-fin.PR`, `q-fin.CP`, `q-fin.MF`

Seed queries:
  - "option pricing implied volatility"
  - "American option Longstaff Schwartz"
  - "Monte Carlo option pricing variance reduction"

Run the bot for this section (writes `papers.md`):

```bash
python run_papers.py
```

## Interconnections
- **Depends on:** [Volatility Modeling & Trading](../02-volatility-modeling), [Machine Learning & Alternative Data](../15-ml-alt-data)
- **Feeds:** [Hedging & Greeks](../03-hedging-greeks), [Market Making](../06-market-making), [Risk Management & Performance Metrics](../11-risk-performance)

See the full interconnected graph in [`../GRAPH.md`](../GRAPH.md) and
[`../graph.html`](../graph.html).
