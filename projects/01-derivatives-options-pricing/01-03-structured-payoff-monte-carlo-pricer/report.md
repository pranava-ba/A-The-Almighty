<!-- cutter-skeleton: report · delete this line once you start writing; scaffold won't overwrite after -->

# Structured-payoff Monte Carlo pricer — Report
*Price knock-in/knock-out (SharkFin-style) payoffs on NIFTY via Monte Carlo, calibrated to the chain-implied surface. · {{ run_id }} · {{ data_version }} · {{ generated }}*
<!-- Title, one-line subtitle, and provenance: run id, data version/fingerprint, and generation timestamp — so a result is always traceable to its inputs. -->

## Verdict
<!-- The one-line answer, highlighted. For a strategy backtest use the controlled vocabulary KEEP / FLAG / SKIP (green / amber / red). For a non-backtest subproject use a short plain verdict (e.g. "matches market IV within 1.2 vol points"). Always state *why* in one clause. -->
```{admonition} Verdict
:class: note
…
```

## Conclusion
<!-- 2–4 sentences: what we found and what it means. This is the whole point of the document — write it so someone can read only this and act. -->
_…_

## Headline metrics
<!-- The handful of numbers that back the verdict. For strategies, route them through the shared tearsheet (net-of-cost return, Sharpe & deflated Sharpe, max drawdown, turnover, trade count). For other work, the equivalent key results (pricing error, R², AUC, reconciliation coverage, etc.). -->
| Key | Value |
|---|---|
|  |  |

## Findings
<!-- The diagnostic answers, as bullets. For strategies, answer the standing questions by default: how many names qualified, how many calls were right vs wrong, what we missed, and any pattern in the right/wrong set. -->
- 

## Critique
<!-- Where to distrust this result: sample size, overfitting risk, data caveats, regime dependence, costs assumed. Honesty here is the point of the whole lab. -->
- 

## Ideas / next  *(optional)*
<!-- Improvements, follow-ups, and open threads. The synthesis/judgement section — good fit for a closing LLM-drafted pass, edited before shipping. -->
- 

## Top configurations  *(optional)*  ·  *backtest only — delete if not a strategy study*
<!-- Best parameter sets after the deflated-Sharpe screen, ranked by net. Keep it to the top handful, not the whole grid. -->
| i | params | n | win% | net | PF | DSR | verdict |
|---|---|---|---|---|---|---|---|

## Right vs wrong (best config)  *(optional)*  ·  *backtest only — delete if not a strategy study*
<!-- The right/wrong breakdown for the single best configuration. -->
| Key | Value |
|---|---|
|  |  |

## Per-symbol (best & worst by net)  *(optional)*  ·  *backtest only — delete if not a strategy study*
<!-- A few best and a few worst names by net — surfaces name-level concentration. -->
| symbol | n | win% | net |
|---|---|---|---|

## Exit mix  *(optional)*  ·  *backtest only — delete if not a strategy study*
<!-- How trades closed (target / stop / time / signal) and the net attributable to each — shows where the edge actually comes from. -->
| reason | n | net |
|---|---|---|

## Most common calls  *(optional)*  ·  *backtest only — delete if not a strategy study*
<!-- Most common right call and most common wrong call, with counts and net. -->
| kind | call | n | wins/losses | net |
|---|---|---|---|---|

## Robustness battery (best config)  *(optional)*  ·  *backtest only — delete if not a strategy study*
<!-- Survivor checks on the best config: trade-order Monte-Carlo, cost ±50%, walk-forward IS/OOS. A fragile KEEP gets downgraded here. -->
| Key | Value |
|---|---|
|  |  |

## Figures  *(optional)*
<!-- Equity curve, per-symbol, exit-mix, parameter-sensitivity — or whatever visual makes the finding obvious. Every figure needs a caption that states its point. -->
![caption](figures/example.png)
