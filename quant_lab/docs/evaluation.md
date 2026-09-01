# The evaluation backbone

Every strategy in the portfolio reports through one library, `evalkit`, so any two are
comparable on identical, honest terms. It is the code form of the {doc}`foundations
<foundations/03_overfitting_and_deflated_sharpe>` ideas.

## Use it

Turn a stream of returns into a scorecard:

```python
from evalkit import tearsheet
t = tearsheet(returns, periods_per_year=252, n_trials=45000, sr_trials_std=0.03)
# {'n', 'ann_return', 'sharpe', 'max_drawdown', 'psr', 'hit_rate', 'deflated_sharpe'}
```

Pass `n_trials` (how many configurations you searched) and the deflated Sharpe drops to
reflect it — the more you tried, the higher the bar. Individual metrics are available too:

```python
from evalkit import sharpe, max_drawdown, deflated_sharpe, turnover, net_returns
from evalkit import purged_kfold, walk_forward

sharpe(returns, periods_per_year=252)
deflated_sharpe(returns, sr_trials_std=0.03, n_trials=45000)
for train, test in purged_kfold(len(returns), k=5, embargo=10):   # leakage-aware CV
    ...
```

**A real example.** SENSEX daily returns (Feb–Aug 2026), pulled from the local seed:

```python
# ann_return = -0.129,  sharpe = -0.74,  max_drawdown = -0.136,
# psr = 0.31,  deflated_sharpe = 0.03   (@ 45,000 trials)
```

The market fell over this window, so the strategy-free benchmark is honestly negative — and
the deflated Sharpe near zero says "no edge here," exactly as it should.

## Understand it

- **Net-of-cost, always.** `net_returns(gross, costs)` is the front door; a Sharpe on gross
  returns is not reported.
- **Deflated Sharpe** ({doc}`derivation <foundations/03_overfitting_and_deflated_sharpe>`) is
  the headline gate. It answers "is this better than the best of `n_trials` coin-flips?",
  correcting for skew, kurtosis, and sample length as well as the search.
- **Leakage-aware CV.** Financial labels overlap in time, so a naive train/test split leaks.
  `purged_kfold` drops the `embargo` bars either side of each test fold from training;
  `walk_forward` uses only the past to judge the future.

:::{admonition} When these metrics mislead
:class: warning
Sharpe and drawdown assume returns that are roughly stationary; across a regime change they
understate risk. Deflated Sharpe needs an honest `n_trials` — undercount your search and you
re-introduce exactly the bias it exists to remove. The metric is a decision aid, not an oracle.
:::
