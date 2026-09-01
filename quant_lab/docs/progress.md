# Progress log

A detailed, dated record of what was done, decided, and why. Newest first. This is a
docs page (folds into the ReadTheDocs site). The forward-looking checklist is
`TODO.md`; the contract is `PORTFOLIO_SPEC.md` (both kept local, not published).

---

## 2026-08-28 — Foundations, scaffolding, governance, cookie cutters

### Decisions locked
| # | Decision | Choice | Rationale |
|---|---|---|---|
| D1 | Repo model | **Monorepo** | one docs site, one graph, one shared `common/` (conv. 5, 9) |
| D2 | Layout | **Hybrid (Option C)** | machinery in `quant_lab/`, deliverables in `projects/`; preserves the graph/registry, keeps imports simple |
| D3 | Granularity | **72 subprojects** (1 per project-idea) | from the 15 sections' project lists in `concepts.json` |
| D4 | Git workflow | **direct to `main`**, CI keeps it green | user preference |
| D5 | Attribution | **no Claude co-author** anywhere | user requirement (conv. 9) |
| D6 | Data sources | Upstox · NSE bhavcopy · yfinance, **stored in DuckDB** | free + primary; DBMS beats loose files |
| D7 | Numbering | topic identity, **build in dependency order** | data section 12 built first |
| D8 | Cookie cutters | share **reading + report + aggregate** as neutral specs | one spec, two renderers (LaTeX ↔ MyST) |
| D9 | Cutter sync | **neutral spec + `sync.py`** | canonical here, mirrored to Bullseye, drift-checked |
| D10 | Aggregate columns | **two column sets** (generic + backtest) by scope | roll-up must work without P&L |

### Built
- **`PORTFOLIO_SPEC.md`** — conventions 1–16, Option C layout, build order, data & house-style rules.
- **`quant_lab/` reshaped to brain-only**; the 15 stale in-place section folders deleted after regeneration.
- **`scaffold.py` (Option C):** one command regenerates the `projects/` tree — 15 section
  landings + **72 subproject folders**, each with a DoD `README.md`, `reading.md`,
  `report.md`, `src/`, `tests/`; plus the graph and the master index.
- **Coverage subsystem** — `coverage.py` parses `RESUME_CONCEPT_TABLES.md` into
  `keyterms.json` (**205 keyterms**: A110 · B28 · C36 · A′17 · B′11 · C′3) and writes
  `coverage.json` + the `coverage.md` scoreboard. Subprojects claim keyterms via
  `covers:[id]` in `concepts.json`. Current coverage **0/205** (nothing built yet).
- **`.gitignore`** — secrets, tokens, the raw-data DBMS, and third-party résumé images all excluded.
- **Cookie cutters** — `quant_lab/cookiecutters/` with the three neutral specs
  (`reading`, `report`, `aggregate`), an architecture README, and `sync.py`. Specs
  **mirrored into Bullseye** (`.../pipeline/cookiecutters/`); drift check passes.
- **Tracking & samples** — this progress page, `TODO.md`, `published-manifest.md`, and
  one filled sample per cutter (`cookiecutters/samples/`) for detailed refinement.

### Notes / gotchas
- **cp1252 wall:** Python's stdout here defaults to cp1252 and crashes on Unicode
  (`→`, `′`). All script runs force `PYTHONUTF8=1 PYTHONIOENCODING=utf-8`; generated
  files are written UTF-8 explicitly.
- The old top-level `p01-market-data-foundation/PROJECT_SPEC.md` actually spans **all of
  section 12** (data lake + tape recorder + option chain + reconciliation), so it's kept
  as reference and will seed `12-01`…`12-05` rather than one folder.

### CI + free-source downloader (2026-08-30)
- **CI** (`.github/workflows/ci.yml`): a tests job (`pytest projects` → 32 pass, offline;
  private adapters/tests are gitignored so CI runs only keyless suites) and a docs job
  (strict `sphinx-build -W`, verified warning-clean). Sanitized progress-page links to
  gitignored files so the public build stays clean.
- **`download.py`**: rebuilds the DuckDB from the free keyless sources (default index/ETF/
  large-cap watchlist); verified live (57 bars). Keeps the repo reproducible without shipping
  data. Deferred: promoting `datalake` → `common/` until the first strategy section imports it.

### Tape + point-in-time, and the docs site (2026-08-30)
- **`12-02` tape** (`datalake.tape`): `TapeRecorder`/`TapeReplay` (NDJSON, gz-aware,
  deterministic ts-ordered replay). **`12-04` point-in-time** (`datalake.pit`):
  survivorship-safe `members_asof` + `adjust_candles` back-adjustment for splits/bonuses/
  dividends. Data-lake suite **25 green**. Section 12 core is now complete.
- **Docs site** (`quant_lab/docs/`, this site): Sphinx + MyST (dollarmath) + RTD theme;
  `.readthedocs.yaml`, from-zero foundations track (backtest / Sharpe / deflated-Sharpe),
  data-foundation + evaluation "use it / understand it" pages, folded concept map, embedded
  interactive graph, glossary, this log. **Builds clean, 13 pages, MathJax math.** Build
  model (a): pre-rendered/committed, generators stay local.

### reconcile + F&O/symbology + eval backbone (2026-08-29)
Three pieces, all with offline tests:
- **`reconcile()`** (`datalake.reconcile`, 12-05): bad-print mask, cross-source close
  mismatch count, gap-fill merge (primary + fill from others), data-quality scorecard.
- **F&O bhavcopy** (`NSEBhavcopySource._parse_fo`/`bhavcopy_fo`): UDiFF FO → canonical with
  OI, instrument_key `NSE_FO|SYM|EXPIRY|STRIKE|CE/PE` (or `|FUT`). **Symbology** (12-03,
  `datalake.Symbology`): NSE↔Upstox `instrument_key`↔ISIN↔Yahoo, from the keyless master.
- **`evalkit`** (11-01, new package): net-of-cost tearsheet — Sharpe, **deflated Sharpe**
  (Bailey–LdP: PSR vs expected-max-Sharpe over N trials), max drawdown, PSR, turnover,
  hit-rate — plus purged K-fold (embargo) + walk-forward CV.
Data-lake suite now **21 green**; evalkit **7 green**. Capstone smoke: SENSEX daily from the
Bullseye seed → tearsheet (ann −12.9%, Sharpe −0.74, DSR 0.03 @ 45k trials) — lake + eval
work together on real data.

### Data audit + Bullseye seed source (2026-08-29)
Audited saved and reachable data (recorded in the internal `DATA_INVENTORY.md`).
Key find: `bullseye_bt.duckdb` (923 MB) `candles` table is schema-identical to ours —
12.3M rows, ~6mo 1-min for ~270 NSE names. Upstox authed NOT reachable here (no
`quant_lab/.env`/token); keyless instrument master works (115,479 instruments). Built
`BullseyeSeedSource` (private) reading that DB read-only + relabeling interval to canonical;
**15 tests green**; live: 375 real 1-min SENSEX bars seeded into a fresh lake. Four sources
now register (bullseye_seed, nse_bhavcopy, upstox, yfinance).

### Data-lake sources: all three adapters (later 2026-08-28)
Upstox token + free sources confirmed by the user. Built the `MarketData` protocol +
registry and **three adapters**: `YFinanceSource` (keyless), `NSEBhavcopySource` (keyless
EOD, UDiFF CM), `UpstoxSource` (**private/gitignored**, token from env). Refactored
`schema` to add `canonical()` (many-instrument frames, e.g. a full bhavcopy). `backfill()`
ties source→store. **12 tests green offline.** Live-verified: yfinance `^NSEI`→DuckDB, and
NSE bhavcopy `2026-08-27` → 3,624 rows with RELIANCE parsed correctly. Upstox stays a
private opt-in smoke (`UPSTOX_ACCESS_TOKEN`). gitignore: `**/sources/upstox_source.py` +
`**/tests/test_upstox.py` private.

### Alternate-page footer + data foundation started (later 2026-08-28)
Added a footer on alternate (even) pages — project title left, `BA Pranava` right — to
`render_latex.py` (so every LaTeX/PDF render gets it) and the reading sample; synced to
Bullseye. Then began **section 12**: `projects/12-…/12-01-unified-data-lake/src/datalake/`
— `schema.py` (normalized candle schema + DuckDB DDL + `normalize()`, tz-aware IST) and
`store.py` (`DuckDBStore` with idempotent ON-CONFLICT upsert); `tests/` 3 green offline
(synthetic fixtures, no network/token). Deps confirmed present: duckdb 1.5.2, yfinance
1.3.0, pandas, pyarrow, curl_cffi. Architecture: core lives in the subproject for now,
promote to `common/marketdata` when a 2nd consumer appears; yfinance/NSE adapters public,
Upstox adapter private. See the subproject `PLAN.md`. Still blocked for live data on the
Upstox-entitlement + free-source answers.

### LaTeX/PDF target + runner (later 2026-08-28)
On feedback that md doesn't show math and a PDF/LaTeX path is needed: built
`render_latex.py` (LaTeX twin of `render_myst.py`, amsmath + Bullseye verdict colours) and
`cut.py` — the runner that **asks/accepts the target** (`github`→MyST for Sphinx, or
`bullseye`→LaTeX→PDF). Verified: `cut.py … --target bullseye --pdf` compiles via pdflatex
(MiKTeX present; no pandoc/tectonic), and a filled `reading.sample.tex` renders the BSM math
to a 2-page PDF. Extended `sync.py` to mirror the whole toolkit (specs + renderers + runner)
to Bullseye. Reminder: MyST math only renders once built (Sphinx→HTML / LaTeX→PDF), never in
a raw-`.md` viewer. Target-label check pending: mapped bullseye→LaTeX/PDF (per "need pdf
latex"), github→Sphinx — confirm the "(md)" wording.

### MyST renderer wired (later 2026-08-28)
Built `cookiecutters/render_myst.py` — turns a shared cutter spec → MyST Markdown (guidance
becomes HTML comments; verdict → admonition; `columns_backtest` noted; `scope='all'` drops
backtest sections). `scaffold.py` now generates each subproject's `reading.md`/`report.md`
**from the specs** (single source of truth) instead of hardcoded stubs, guarded by a line-1
`cutter-skeleton` marker so authored docs are never overwritten. Migrated all 72×2 stubs.
Bullseye keeps the parallel `render_latex.py` (still to build) reading the same specs.

### Publish policy locked (later 2026-08-28)
Public repo narrowed to **README + LICENSE + 72 projects' code + `common/` +
`requirements.txt` + docs**. Local-only: planning (`PORTFOLIO_SPEC`, `TODO`), machinery
(`concepts.json`, `scaffold.py`, `coverage.*`, `keyterms.json`, cookiecutters, raw graph),
the corpus (`RESUME_*`, résumé images), and **all data including samples**. Concept
tables + graph + progress **fold into RTD**. Streamlit avoided unless necessary.
Consequence: convention 11 reworked — reproducibility via free keyless sources +
synthetic test fixtures, not shipped samples. See `published-manifest.md`.

### Still open
- Refine the 3 cookie cutters against the samples.
- **How RTD is built** given the machinery isn't public (ship rendered docs vs private docs source).
- Upstox entitlement + free-source confirmation (blocks the live-data parts of section 12).

<!-- Next entry goes ABOVE this line. Keep entries dated and specific: what changed,
     what was decided, and why — enough that a reader a month later can reconstruct it. -->
