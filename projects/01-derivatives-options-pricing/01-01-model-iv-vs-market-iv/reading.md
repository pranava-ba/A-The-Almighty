# Model-IV vs market-IV surface — Reading

*Price NIFTY/BANKNIFTY options with BSM, CRR and trinomial trees, invert each quote for
its implied volatility, and read the gap between a flat-vol model and the market as the
volatility surface. · 01-01 · derivatives & options pricing*

## Motivation

An option's price is one number; the market's *view* is a surface. Black-Scholes-Merton
(BSM) maps a single volatility $\sigma$ to a price, so the price of a traded option can be
run backwards through the same formula to recover the one volatility that reproduces it —
its **implied volatility** (IV). Do that for every strike $K$ and expiry $T$ on the board
and you get the **implied-volatility surface** $\sigma_{\text{mkt}}(K,T)$.

If BSM's assumptions held, that surface would be flat: one $\sigma$ for all strikes. It is
never flat. The shape of $\sigma_{\text{mkt}}(K,T)$ — the **smile/skew** — is exactly the
market pricing in everything BSM leaves out (fat tails, stochastic vol, jumps, crash-risk
premium). This subproject builds the machinery to measure that gap honestly: a correct
pricer, a robust inverter, and a diff surface that lays *model IV* next to *market IV*
across the whole grid. Get the pricer or the inverter subtly wrong and every downstream
signal — vol carry, skew trades, hedging ratios — inherits the error, so the emphasis here
is on numerical correctness that is *tested*, not asserted.

## Theory & derivation

### Risk-neutral pricing and the BSM PDE

Under the risk-neutral measure $\mathbb{Q}$, the underlying follows a geometric Brownian
motion with drift equal to the cost of carry $r-q$ ($r$ = risk-free rate, $q$ = continuous
dividend yield):

$$ dS_t = (r-q)\,S_t\,dt + \sigma S_t\,dW_t^{\mathbb{Q}}. $$

By Feynman-Kac, the price $V(S,t)$ of any European claim solves the **BSM PDE**

$$ \frac{\partial V}{\partial t} + \tfrac12 \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2}
   + (r-q) S \frac{\partial V}{\partial S} - rV = 0, $$

with the payoff as terminal condition. Equivalently, the price is the discounted
risk-neutral expectation $V = e^{-r\tau}\,\mathbb{E}^{\mathbb{Q}}[\,\text{payoff}\,]$ with
$\tau = T-t$ the time to expiry.

### Closed form and the Greeks

For a vanilla call/put ($\phi=+1$ for a call, $-1$ for a put) the expectation integrates to

$$ V = \phi\left[ S e^{-q\tau} N(\phi d_1) - K e^{-r\tau} N(\phi d_2)\right], \qquad
   d_{1,2} = \frac{\ln(S/K) + (r-q \pm \tfrac12\sigma^2)\tau}{\sigma\sqrt{\tau}}. $$

Differentiating gives the **Greeks** the code returns (call forms; put via $\phi$):

| Greek | Formula | Meaning |
|---|---|---|
| Delta $\Delta$ | $\phi e^{-q\tau} N(\phi d_1)$ | ∂price/∂spot |
| Gamma $\Gamma$ | $e^{-q\tau} n(d_1)/(S\sigma\sqrt{\tau})$ | ∂²price/∂spot² |
| Vega $\nu$ | $S e^{-q\tau} n(d_1)\sqrt{\tau}$ | ∂price/∂vol (per 1.00) |
| Theta $\Theta$ | $-\frac{S e^{-q\tau} n(d_1)\sigma}{2\sqrt\tau} - \phi r K e^{-r\tau}N(\phi d_2) + \phi q S e^{-q\tau} N(\phi d_1)$ | calendar decay |
| Rho $\rho$ | $\phi K \tau e^{-r\tau} N(\phi d_2)$ | ∂price/∂rate |

where $N$ and $n$ are the standard-normal CDF and PDF. Vega and Gamma are
kind-independent; $\Theta$ is the derivative w.r.t. *calendar* time, i.e.
$-\partial V/\partial\tau$, hence negative for most long options. Each formula is checked
against a central finite difference of the price in the tests, which is the cheapest
guard against an algebra slip.

### Inverting for implied volatility

$V(\sigma)$ is continuous and strictly increasing in $\sigma$ on $(0,\infty)$ with vega as
its slope, so the market IV is the unique root of $f(\sigma)=V_{\text{BSM}}(\sigma) -
V_{\text{mkt}}$. We solve it with **Newton-Raphson**,

$$ \sigma_{n+1} = \sigma_n - \frac{V_{\text{BSM}}(\sigma_n) - V_{\text{mkt}}}{\nu(\sigma_n)}, $$

seeded by the Brenner-Subrahmanyam ATM approximation $\sigma_0 \approx
\sqrt{2\pi/\tau}\,\,V_{\text{mkt}}/S$. Newton is quadratically convergent where vega is
healthy but stalls in the deep wings and near expiry, where $\nu\to 0$; there the solver
falls back to **Brent's method** on the bracket $[\sigma_{\min},\sigma_{\max}]$, which
cannot leave the interval. Before solving, a **no-arbitrage screen** rejects the
un-invertible: a price at or below intrinsic implies $\sigma=0$, and a price above the
trivial upper bound ($Se^{-q\tau}$ for a call, $Ke^{-r\tau}$ for a put) has no real IV and
returns `NaN` with a reason rather than diverging.

### Lattice pricers and convergence

The **Cox-Ross-Rubinstein (CRR)** binomial tree discretises $[0,\tau]$ into $N$ steps with

$$ u = e^{\sigma\sqrt{\Delta t}},\quad d = 1/u,\quad
   p = \frac{e^{(r-q)\Delta t} - d}{u - d}, $$

then values the option by backward induction, discounting expected continuation by
$e^{-r\Delta t}$ at each node. It converges to BSM as $N\to\infty$ at rate $O(1/N)$ (with
the familiar even/odd oscillation). The **Boyle trinomial** tree adds a middle branch
($u=e^{\sigma\sqrt{2\Delta t}}$, $m=1$, $d=1/u$ with Boyle's probabilities); the extra
degree of freedom gives smoother, faster convergence per step for European payoffs. The
lattices matter because they extend cleanly to **American** exercise: replace the node
value with $\max(\text{continuation},\ \text{intrinsic})$. This makes
$V_{\text{Amer}}\ge V_{\text{Euro}}$ by construction, the gap being the **early-exercise
premium** — zero for a non-dividend American call (never optimal to exercise early),
strictly positive for a sufficiently in-the-money American put under a positive rate.

### The surface as model error, and the model-free forward

Reprice the whole chain at a *single* vol per expiry and the residual
$\sigma_{\text{mkt}}(K,T) - \sigma_{\text{model}}$ **is** the smile — the documented failure
of flat-vol BSM, displayed as a surface rather than hidden in a price. To place strikes on
that surface we need the forward $F$. Rather than trust a possibly mis-matched future
(index options list weekly, index futures monthly), we recover $F$ **model-free** from
put-call parity,

$$ C(K) - P(K) = (F - K)\,e^{-r\tau} \;\Longrightarrow\; F = K + e^{r\tau}\big(C(K)-P(K)\big), $$

averaged over near-the-money strikes. Options on the same expiry are then priced in the
forward measure (setting spot $=F$, $q=r$ reduces BSM exactly to Black-76), which removes
any spot/basis ambiguity from the recovered IVs.

## Assumptions & notation

| Key | Value / meaning |
|---|---|
| $S,\,F$ | spot, forward ($F = S e^{(r-q)\tau}$) |
| $K,\,\tau$ | strike, time to expiry in years (ACT/365) |
| $r,\,q$ | risk-free rate, continuous dividend yield (flat, per expiry) |
| $\sigma$ | Black-Scholes volatility (annualised) |
| $\phi$ | $+1$ call, $-1$ put |
| $N,n$ | standard-normal CDF, PDF |
| Frictions | none in-model; market frictions surface *as* the smile, not as inputs |

The working assumptions are BSM's: continuous trading, constant $\sigma$ and $r$ over the
life of the option, GBM dynamics, no transaction costs. The whole point of the diff
surface is to *measure where these break*, so they are named, not defended.

## How we applied it

The engine lives in the promotable package **`optkit`** (`bsm`, `lattice`, `iv`), with a
subproject-specific surface layer (`chain`, `surface`). Everything is vectorised over a
chain, so a full board prices and inverts in one call. Three data paths, in decreasing
order of what this machine can run:

- **Synthetic (always).** `synthetic_smile_chain` plants a quadratic-in-log-moneyness
  smile, prices it with BSM, and hands back both the prices and the true IVs — so the
  tests can assert that inversion recovers the input to machine precision and that a flat
  model reproduces the planted skew. No network, no token (convention 11).
- **NSE F&O bhavcopy (keyless).** `OptionChain.from_fo_frame` turns the data lake's free
  EOD F&O bhavcopy (settlement prices + OI) into a chain; market IV is then inverted. This
  is the offline stand-in for a live chain and is how the report's real NIFTY smile is
  produced.
- **Upstox chain (token, optional).** When a token exists, the broker publishes its own IV
  and Greeks; `attach_broker` diffs ours against theirs. This path needs an entitlement
  this machine does not have, so it is never exercised by the offline tests.

## Data

NIFTY/BANKNIFTY options via **NSE F&O bhavcopy** (free, keyless EOD, UDiFF F&O format —
settlement `ClsPric`, open interest) and, when entitled, the **Upstox** option chain.
Forwards are recovered from put-call parity and cross-checked against the listed monthly
future. Nothing is committed; the smile is reproduced by pulling a bhavcopy date through
the data lake's keyless source.

## Worked example / intuition

Take a single expiry. Read off the strike where a call and a put cost the same amount:
that is (near enough) the forward, and no model was used to find it. Now walk down in
strike. Each out-of-the-money put you pass is priced by the market as if volatility were a
little higher than the last — buyers pay up for crash protection. Invert each price and
the numbers you get *rise* as you descend: the **downside skew**. Walk up in strike
instead and IV rises again, more gently: the **smile**. A flat-vol model draws a
horizontal line through the middle of this; the vertical distance from that line to the
market points, strike by strike, is precisely what this subproject computes and what every
volatility strategy in later sections trades against.

## References & harvested papers

- Black, F. & Scholes, M. (1973). *The Pricing of Options and Corporate Liabilities.* JPE.
- Merton, R. (1973). *Theory of Rational Option Pricing.* Bell J. Econ. — dividend yield $q$.
- Cox, J., Ross, S. & Rubinstein, M. (1979). *Option Pricing: A Simplified Approach.* — CRR tree.
- Boyle, P. (1986/1988). *Option Valuation Using a Three-Jump Process* / *A Lattice Framework.* — trinomial.
- Brenner, M. & Subrahmanyam, M. (1988). *A Simple Formula to Compute the IV.* — the Newton seed.
- Breeden, D. & Litzenberger, R. (1978). *Prices of State-Contingent Claims Implicit in Option Prices.* — the risk-neutral density (built in [01-05](../01-05-risk-neutral-valuation-from-first)).
- Gatheral, J. (2006). *The Volatility Surface.* — the object this subproject measures.

## See also

- Feeds [02 · volatility modeling](../../02-volatility-modeling) — the surface measured here
  is what a SABR/SVI/stochastic-vol model is fit to.
- Shares the pricing core with the other section-01 subprojects:
  [01-02 American vs European](../01-02-american-vs-european-premium),
  [01-04 finite-difference PDE](../01-04-finite-difference-bs-pde-pricer),
  [01-05 risk-neutral density](../01-05-risk-neutral-valuation-from-first).
- Data path: [12-01 unified data lake](../../12-asset-classes-data-infra/12-01-unified-data-lake).
