# The concept map

The portfolio is built to cover, at least once and in real code, a broad map of quantitative
finance — decomposed into **financial concepts** (what), the **mathematics & statistics**
behind them (how), and the **technical stack** that implements them (with what). A machine-
checked coverage tool tracks that every one of these is exercised somewhere.

## Table A — Financial concepts

The primary map: every distinct model, instrument, strategy, and metric, grouped by area.

| Area | Examples |
|---|---|
| Derivatives & options pricing | Black–Scholes–Merton, binomial/trinomial trees, Monte-Carlo & LSMC, finite-difference PDEs, structured payoffs, risk-neutral densities |
| Volatility modeling & trading | realized-vol estimators, India VIX regimes, SABR / SVI surfaces, rough volatility (Hurst), Heston, jump-diffusion |
| Hedging & Greeks | delta hedging, hedge-effectiveness grids, tail hedging, deep/RL hedging |
| Systematic strategies | momentum, mean-reversion, regime-switching, event studies, cross-market contagion |
| Statistical arbitrage | cointegration pairs, index-futures basis, ETF-vs-basket, OU bands, Kalman hedge ratios |
| Market making | Avellaneda–Stoikov, inventory-aware quoting, adverse selection, Hawkes order flow |
| Microstructure & execution | Almgren–Chriss, order-book imbalance / micro-price, impact & slippage, liquidity regimes |
| Portfolio construction | mean–variance + shrinkage, risk parity, Black–Litterman, HRP, mean-CVaR |
| Factor / alpha research | multi-factor models, news-sentiment (FinBERT), Fama–MacBeth, overfit-aware search |
| Fixed income & credit | yield curves, ML default models, Jarrow–Lando–Turnbull, risk-neutral vs real-world |
| Risk & performance | VaR / expected shortfall, EVT tails, copula tail-dependence, the shared tearsheet |
| Data & infrastructure | the unified lake, tape recorder/replay, symbology, point-in-time universe, reconciliation |
| Corporate finance & valuation | comps, DCF (+ Monte-Carlo & reverse), filings NLP, real options |
| Market simulation | LOB simulators, heterogeneous-agent markets, Kyle-informed traders, stylized-facts calibration |
| Machine learning & alt-data | sequence models, sentiment pipelines, generative scenarios for risk |

## Table B — Mathematics & statistics

Stochastic processes & SDEs · change of measure (Girsanov) & Feynman–Kac · Monte-Carlo &
variance reduction · time-series (Kalman, ARIMA, GARCH) · regression & penalization ·
convex & robust optimization · extreme-value theory & copulas · Markov / regime-switching ·
cointegration & stationarity · dimensionality reduction · information theory · hypothesis
testing & multiple-comparisons control.

## Table C — Technical & computational

Python (NumPy/Pandas/SciPy) · DuckDB & SQL · vectorized backtesting engines · scikit-learn
& tree ensembles · deep learning (PyTorch) · NLP / LLMs (FinBERT) · reinforcement learning ·
big-data / tick-data engineering · reproducible reporting (this site + LaTeX/PDF) · CI.

## Beyond the baseline

The lab deliberately reaches past the "standard" list into harder, graduate-level machinery —
deep hedging, execution as a Markov decision process, information-based microstructure (Kyle,
Glosten–Milgrom, Hawkes), financial-contagion identification, deflated-Sharpe / probability of
backtest overfitting, EVT VaR/ES with copula tail-dependence, and point-in-time data integrity.

*Coverage of every item is tracked mechanically; see the {doc}`graph` for how the pieces
connect.*
