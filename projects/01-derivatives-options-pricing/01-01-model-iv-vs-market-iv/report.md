# Model-IV vs market-IV surface — Report

*Price NIFTY options with BSM/CRR/trinomial, invert every quote for IV, and diff the
market surface against a flat-vol model. · run: NIFTY 2026-09-04 EOD · data: NSE F&O
bhavcopy (keyless) + synthetic fixtures · generated 2026-09-06*

## Verdict

```{admonition} Verdict
:class: note
**Pricers and inverter validated.** On live NIFTY F&O the put-call-parity forward matches
the listed monthly future to **−2.56 index points (−0.011%)**, and inversion recovers a
clean equity skew across **97 strikes** with no ATM±10% failures. On synthetic quotes the
IV round-trip is exact to **1e-6** and CRR/trinomial track closed-form BSM to **< 0.006**.
```

## Conclusion

The engine reproduces the market it is pointed at. The strongest evidence is not a
synthetic test but a real one: recovering the forward from option prices alone (put-call
parity) lands within three index points of the exchange's own futures settlement, which
means the pricing conventions, day-count, and discounting are internally consistent on
real data. With the forward pinned, the inverted NIFTY surface is a textbook downside
skew — out-of-the-money puts imply ~9.5 vol points more than the at-the-money — exactly
the object the volatility-modeling section (02) will fit. The flat-vol model's error
*is* that skew, and the diff surface measures it strike by strike.

## Headline metrics

| Key | Value |
|---|---|
| Live snapshot | NIFTY, 2026-09-04 EOD, expiry 2026-09-29 (25 days) |
| Forward — parity vs future | 24,050.66 vs 24,048.10  → **−2.56 (−0.011%)** |
| ATM implied vol | 9.5158% |
| IV at 90% / 110% strike | 19.0733% / 15.4255% |
| Downside skew (IV₉₀ − IV₁₁₀) | **+3.6478 vol points** |
| Strikes inverted (ATM±10%) | 97, zero failures |
| Synthetic IV round-trip (max\|BSM(σ)−mkt\|) | 0.000000 |
| Synthetic IV RMSE vs flat model | 0.030049 (lower/atm/upper 0.0443 / 0.0037 / 0.0083) |
| BSM vs CRR & trinomial (max abs) | 0.005627 |
| American put early-exercise premium¹ | +3.018774 |

<sub>¹ S=80, K=100, r=8%, σ=30%, T=1y: European 17.567049 → American 20.585823.</sub>

## Findings

- **Model-free forward ≈ listed future.** $F = K + e^{r\tau}(C-P)$ over near-ATM strikes
  gives 24,050.66 against the 2026-09-29 future's 24,048.10 — a −0.011% basis. Recovering
  the forward *without* a model, and having it agree with the exchange, validates the
  discounting/day-count end to end on real data.
- **The surface is a clean equity skew.** ATM IV 9.52%; the 90%-strike put implies 19.07%
  and the 110%-strike call 15.43% — both wings up, the downside steeper. No smoothing was
  applied; this is raw settlement-price inversion.
- **Inversion is exact where it should be.** On synthetic quotes with a planted smile,
  `BSM(σ_inverted)` reprices every quote to 0.000000 and recovers the planted σ to
  ~1e-10; the deep-wing quotes correctly route through the Brent fallback.
- **Lattices agree with closed form.** CRR error falls ~O(1/N) (−0.0055 at 256 steps,
  −0.0014 at 1024), trinomial ~2× tighter per step; both within 0.006 of BSM on the ATM
  benchmark. American ≥ European everywhere; the non-dividend American call equals its
  European twin, and the ITM American put carries a real +3.02 early-exercise premium.
- **A flat model's residual is the smile.** With `model_iv="atm"`, the diff surface is
  ~0 at the money and grows into both wings (lower-wing MAE 0.044 vs upper-wing 0.008),
  i.e. the model error *is* the skew — the intended headline.

## Critique

- **Settlement, not last-traded, prices.** NSE F&O bhavcopy carries end-of-day settlement
  `ClsPric`, which for illiquid strikes is a theoretical mark, not a trade. Deep-wing IVs
  inherit that; the report deliberately restricts to the ATM±10% band and drops
  sub-₹0.50 prints.
- **No broker cross-check here.** The headline concept — diffing our IV/Greeks against the
  *broker's published* IV/Greeks — needs the live Upstox chain, which this machine has no
  token for. `attach_broker` implements it but is unexercised offline; the validation
  above is against put-call parity and the futures forward instead.
- **Flat term-structure of $r$ and $q$.** A single $r$ (6.5%) and $q=r$ (forward pricing)
  per expiry. Fine for a one-expiry smile snapshot; a full surface across expiries wants a
  proper discount curve and dividend schedule.
- **Single snapshot, short-dated.** One EOD, one 25-day expiry. Nothing here speaks to
  term structure or time stability; that is section 02's job, fed by this surface.
- **ACT/365 day-count** and calendar-day TTM ignore the intraday decay of the last
  session — negligible at 25 days, not at 2.

## Ideas / next

- Wire the **Upstox chain path** end to end once a token is available and turn
  `attach_broker` into a standing our-IV-vs-broker-IV/Greeks scorecard.
- Fit **SVI/SABR** to the inverted surface (hands off to [02](../../02-volatility-modeling))
  and report calendar/butterfly **no-arbitrage** violations as a data-quality gate.
- Extend to **BANKNIFTY** and to a multi-expiry pull so the term structure of ATM vol and
  skew can be tracked, not just a single slice.

## Reproduce

```bash
pip install -r requirements.txt
python -m pytest projects/01-derivatives-options-pricing/01-01-model-iv-vs-market-iv/tests -q
```

The synthetic results and every test run offline with no token. The live NIFTY smile is
reproduced by pulling any recent NSE F&O bhavcopy date through the data lake's keyless
`NSEBhavcopySource.bhavcopy_fo(date)` and inverting with `optkit.implied_vol_chain`.
