<div align="center">

<pre>
    _      _____ _   _ _____      _    _     __  __ ___ ____ _   _ _______   __
   / \    |_   _| | | | ____|    / \  | |   |  \/  |_ _/ ___| | | |_   _\ \ / /
  / _ \     | | | |_| |  _|     / _ \ | |   | |\/| || | |  _| |_| | | |  \ V /
 / ___ \    | | |  _  | |___   / ___ \| |___| |  | || | |_| |  _  | | |   | |
/_/   \_\   |_| |_| |_|_____| /_/   \_\_____|_|  |_|___\____|_| |_| |_|   |_|
</pre>

**A — The Almighty**

<br/>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-8B949E?style=flat-square)](LICENSE)
[![CI](https://github.com/pranava-ba/A-The-Almighty/actions/workflows/ci.yml/badge.svg)](https://github.com/pranava-ba/A-The-Almighty/actions/workflows/ci.yml)

[![Docs](https://img.shields.io/badge/📖%20Documentation-ReadTheDocs-1ABC9C?style=for-the-badge&logo=readthedocs&logoColor=white)](https://a-the-almighty.readthedocs.io)

<br/>

*A quantitative-finance research portfolio — 72 self-contained projects across 15 topic
sections, on one shared data lake and one leakage-aware evaluation backbone.*

<sub>Named for Yhwach's Schrift in <em>Bleach</em> — <strong>「A」— The Almighty</strong>, the power to
perceive and rewrite every future. A fitting standard for the work here: forecasting
markets honestly, and measuring exactly how far that sight really reaches.</sub>

</div>

<br/>

---

## About

**A — The Almighty** is a monorepo of graduate-level quant projects, each shipping working
code, tests, and written theory + results. Every project is built on two shared
foundations so results are comparable and hard to fool:

- **One data lake** — a DuckDB store with a `MarketData` adapter protocol over free,
  keyless sources (yfinance, NSE bhavcopy), plus symbology, tape/replay, point-in-time
  universes, and corporate-action back-adjustment.
- **One evaluation backbone** — net-of-cost tearsheets (Sharpe, **deflated** Sharpe, PSR,
  max-drawdown, turnover, hit-rate) and leakage-aware validation (purged K-fold with
  embargo, walk-forward).

The concept map behind the sections is distilled from a corpus of quant résumés and
deliberately pushed past it — see the documentation.

---

## Installation

<details>
<summary><strong>🐍 Run from Source</strong></summary>
<br/>

Requires Python 3.10+.

```bash
git clone https://github.com/pranava-ba/A-The-Almighty.git
cd A-The-Almighty
pip install -r requirements.txt
python -m pytest projects -q      # run the offline, keyless test suites
```

</details>

---

## Quick Start

| Step | Action |
|------|--------|
| 1 | `pip install -r requirements.txt` |
| 2 | Browse a section under `projects/NN-*/` — each subproject has `src/`, `tests/`, `reading.md` (theory), `report.md` (results). |
| 3 | Run the shared test suites: `python -m pytest projects -q`. |
| 4 | Read the [documentation](https://a-the-almighty.readthedocs.io) for the concept map, data/eval design, and per-project write-ups. |

---

## Layout

```
projects/NN-section/NN-MM-slug/   # the 72 deliverables (src · tests · reading.md · report.md)
  01-derivatives-options-pricing     06-market-making                 11-risk-performance
  02-volatility-modeling             07-microstructure-execution      12-asset-classes-data-infra
  03-hedging-greeks                  08-portfolio-optimization        13-corporate-finance-valuation
  04-systematic-trading              09-factor-alpha-research         14-market-simulation-abm
  05-statistical-arbitrage           10-fixed-income-credit           15-ml-alt-data
quant_lab/docs/                   # ReadTheDocs source (concept map, foundations, glossary)
requirements.txt · LICENSE
```

Section numbers are **topic identity, not build order** — the data foundation (§12) and the
shared evaluation library (§11) are built first; everything else depends on them.

---

## Features

<details>
<summary><strong>🏗️ Shared foundations</strong></summary>
<br/>

- **`datalake` (§12-01)** — DuckDB store + `MarketData` protocol; adapters for yfinance and
  NSE bhavcopy (live-verified); reconcile (bad-print detection + gap-fill), symbology
  (NSE ↔ ISIN ↔ Yahoo + F&O open-interest), tape record/replay, and point-in-time universe
  with corporate-action back-adjustment.
- **`evalkit` (§11-01)** — net-of-cost tearsheet (Sharpe, deflated Sharpe, PSR, max-DD,
  turnover, hit-rate) + purged K-fold / embargo / walk-forward cross-validation.

</details>

<details>
<summary><strong>🔬 Research standards</strong></summary>
<br/>

- Survivorship-bias-free, point-in-time data; alpha reported **net of costs**.
- Leakage-aware validation everywhere; overfitting controlled (deflated Sharpe, PBO).
- A machine-checked keyterm coverage matrix keeps the portfolio honest about what it covers.
- Reproducible by a stranger: free keyless sources + synthetic test fixtures — no data is shipped.

</details>

---

## Data Notes

> No market data is shipped. Tests run offline against synthetic fixtures and free, keyless
> sources; nothing here requires a paid feed or an API token. Some private adapters
> (broker-token and local-seed sources) are kept out of this repository, so the public code
> is fully **readable** but a few live data paths are not runnable without that private layer
> — an intentional trade-off for a public showcase.

---

<div align="center">

**Pranava BA** · © 2026 · [MIT License](LICENSE)

</div>
