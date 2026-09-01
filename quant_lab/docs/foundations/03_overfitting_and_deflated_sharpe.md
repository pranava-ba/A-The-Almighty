# Overfitting, and the Deflated Sharpe

**The core danger.** If you try 1,000 random strategies on the same history, a few will look
spectacular *by pure chance* — the way someone in a big enough room will flip ten heads in a
row. Pick the best-looking one and you've "discovered" nothing but noise. This is
**overfitting**, and with computers testing thousands of parameter combinations, it is the
default outcome, not the exception.

**The honest question** is therefore not *"is this Sharpe high?"* but *"is this Sharpe high
**given how many things I tried**?"*

**Probabilistic Sharpe Ratio (PSR).** First, account for sample size and shape. A Sharpe from
few, fat-tailed, skewed returns deserves less trust. PSR converts a Sharpe into a
*probability* that the true Sharpe beats a benchmark, correcting for skew $\gamma_3$,
kurtosis $\gamma_4$, and sample length $n$:

$$\text{PSR}(SR^\*) = \Phi\!\left(\frac{(\widehat{SR} - SR^\*)\sqrt{n-1}}{\sqrt{1 - \gamma_3 \widehat{SR} + \frac{\gamma_4 - 1}{4}\widehat{SR}^2}}\right)$$

**Deflated Sharpe Ratio (DSR).** Then account for the *search*. Set the benchmark $SR^\*$ not
to zero but to the Sharpe you'd *expect to see by luck alone* as the best of $N$ tries — which
grows with $N$. Clear that bar and you likely have something; fail it and your "edge" was the
room full of coin-flippers.

| Plain English | Formal |
|---|---|
| how good, adjusted for shape & length | PSR |
| the bar luck alone would clear over $N$ tries | $SR_0 = \sqrt{V}\left[(1-\gamma)\,Z^{-1}(1-\tfrac1N) + \gamma\,Z^{-1}(1-\tfrac1{Ne})\right]$ |
| the honest verdict | $\text{DSR} = \text{PSR}(SR_0)$ |

($V$ = variance of the trial Sharpes, $\gamma \approx 0.5772$ the Euler–Mascheroni constant,
$Z^{-1}$ the inverse normal CDF.)

This is why, in this portfolio, a strategy's report leads with a **verdict** (KEEP / FLAG /
SKIP) driven by the DSR, not the raw Sharpe — and why searching harder makes the bar *higher*,
not lower. Both PSR and DSR are implemented in {doc}`../evaluation`.

:::{admonition} The takeaway
:class: tip
A backtest number means nothing without the count of how many were tried to find it. Honesty
about that count is the difference between research and self-deception.
:::
