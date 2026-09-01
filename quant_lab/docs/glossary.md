# Glossary

```{glossary}
Backtest
  A simulation of a trading rule against historical data, built to be pessimistic and honest
  about costs, look-ahead, and survivorship. See {doc}`foundations/01_what_is_a_backtest`.

Return
  The fractional change in value over a period; compounding $\prod_t(1+r_t)$ gives growth.

Sharpe ratio
  Reward per unit of risk: mean excess return divided by its standard deviation, annualized.
  See {doc}`foundations/02_returns_and_sharpe`.

Drawdown
  The worst peak-to-trough decline in cumulative equity — the loss a holder would have suffered.

Overfitting
  Mistaking noise for signal by selecting the best of many strategies tried on the same data.

PSR
  Probabilistic Sharpe Ratio — the probability the true Sharpe beats a benchmark, correcting
  for skew, kurtosis, and sample length.

Deflated Sharpe (DSR)
  A PSR whose benchmark is the Sharpe expected by luck as the best of $N$ trials; the headline
  honesty gate. See {doc}`foundations/03_overfitting_and_deflated_sharpe`.

Point-in-time
  Using only information knowable at a given historical moment — including which stocks were
  in an index then — to avoid look-ahead and survivorship bias.

Survivorship bias
  The error of testing only on instruments that still exist today, silently excluding failures.

Instrument key
  The portfolio's canonical identifier for a tradable instrument, normalized across sources by
  the {doc}`symbology layer <data_foundation>` (e.g. `NSE_INDEX|Nifty 50`).

Bhavcopy
  NSE's official end-of-day file of every instrument's OHLC (and, for F&O, open interest).

Open interest (OI)
  The number of derivative contracts outstanding — a positioning signal unique to F&O.

Implied volatility (IV)
  The volatility that makes a pricing model reproduce an option's market price; the market's
  forward-looking risk estimate.

Tearsheet
  The standard one-page scorecard (return, Sharpe, deflated Sharpe, drawdown, turnover) every
  strategy reports through. See {doc}`evaluation`.
```
