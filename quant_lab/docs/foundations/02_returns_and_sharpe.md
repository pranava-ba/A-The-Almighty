# Returns, risk, and the Sharpe ratio

**Return** is just the percentage change in your money. If ₹100 becomes ₹101, that period's
return is $r = 0.01$ (1%). String these together and the growth of ₹1 is the compound
product $\prod_t (1 + r_t)$.

**Risk**, here, means *variability* — how much the returns bounce around. Two strategies can
earn the same average and feel completely different: one drifts smoothly up, the other lurches.
We measure that bounce with the standard deviation $\sigma$ of the returns.

**The Sharpe ratio** combines the two into one number: reward per unit of risk.

$$\text{Sharpe} = \frac{\bar{r} - r_f}{\sigma} \times \sqrt{P}$$

| Plain English | Formal |
|---|---|
| average return, above cash… | $\bar r - r_f$ (mean excess return) |
| …divided by how bumpy it is… | $\sigma$ (std of returns) |
| …scaled to a yearly figure | $\sqrt{P}$, $P$ = periods per year (252 for daily) |

A Sharpe of 1 is decent; above 2, net of costs, is genuinely good and rare. The scaling by
$\sqrt{P}$ is why you must say the frequency — a "Sharpe of 3" on 1-minute data is not the
same animal as one on daily data.

**Drawdown** is the other number that matters to a human: the worst peak-to-trough fall in
your equity. A strategy with a great Sharpe and a 60% drawdown is un-tradeable, because you'd
have quit before the recovery.

:::{admonition} Why Sharpe isn't enough
:class: warning
Sharpe rewards a smooth line, but it's computed from a *sample*, and short samples are noisy.
A high Sharpe from 30 trades might be luck. The next page is about not being fooled by it.
:::

These are exactly the numbers the {doc}`../evaluation` tearsheet computes.
