# What is a backtest?

**Plain English.** A backtest asks: *"if I had followed this rule in the past, what would
have happened?"* You take a trading rule ("buy when the price crosses above its 20-day
average"), replay it over historical prices, and add up the profits and losses.

**Why it's harder than it sounds.** The past is the only data you have, and it's easy to
cheat without meaning to. Three traps this portfolio takes seriously:

- **Look-ahead bias** — using information you couldn't have known yet (today's closing price
  to decide today's open trade). A backtest must only ever see what was knowable *at the
  time*. This is why the data layer has a {doc}`point-in-time <../data_foundation>` universe.
- **Survivorship bias** — testing on the companies that exist *today*. The winners survived;
  the failures dropped out of your list. Backtest on today's Nifty 50 and you've quietly
  excluded every company that went bust. The fix is point-in-time index membership.
- **Costs** — every trade pays a spread, brokerage, and slippage. A strategy that trades a
  lot can look great gross and lose money net. Every result here is reported **net of costs**.

**The deliverable.** A backtest produces a stream of returns, which we summarize in a
{doc}`tearsheet <../evaluation>` — the standard scorecard (return, risk, drawdown) that
lets any two strategies be compared on the same terms.

:::{admonition} The one-sentence version
:class: note
A backtest is a simulation of a rule against history; its job is to be *pessimistic and
honest*, because the market will be.
:::
