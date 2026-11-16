# Black-Scholes Options Pricer

Prices European call and put options with the Black-Scholes model, computes all
five Greeks, and solves for implied volatility. A vectorised NumPy pricing
engine with a Streamlit front end.

**[Live demo →](https://black-scholes-pricer-finn.streamlit.app)**

![App screenshot](docs/screenshot.png)

## Features

- **Pricing:** European calls and puts, with a continuous dividend yield
- **Greeks:** delta, gamma, vega, theta and rho, in trader units (vega and rho
  per 1%, theta per day)
- **Implied volatility:** recovers the volatility implied by a market price,
  using Newton-Raphson safeguarded by bisection, with no-arbitrage bound checks
- **Charts:** price sensitivity to every input, each Greek against spot, and
  price heatmaps across spot and volatility
- **Vectorised engine:** every function accepts scalars or NumPy arrays and
  broadcasts them, so a whole heatmap is priced in one call with no Python loops
- **Tested:** reference values, put-call parity, finite-difference checks on
  every Greek, and implied-vol round trips

## The maths

<details>
<summary>Pricing formula, Greeks and implied volatility</summary>

$$C = S e^{-qT} N(d_1) - K e^{-rT} N(d_2)$$

$$P = K e^{-rT} N(-d_2) - S e^{-qT} N(-d_1)$$

$$d_1 = \frac{\ln(S/K) + \left(r - q + \tfrac{1}{2}\sigma^2\right)T}{\sigma\sqrt{T}}, \qquad d_2 = d_1 - \sigma\sqrt{T}$$

where $S$ is the spot price, $K$ the strike, $T$ the time to expiry in years,
$r$ the risk-free rate, $q$ the dividend yield, $\sigma$ the volatility and $N$
the standard normal CDF.

**Reading the formula:** $N(d_2)$ is the risk-neutral probability that the
option finishes in the money, so $K e^{-rT} N(d_2)$ is the present value of the
strike you expect to pay. $e^{-qT} N(d_1)$ is the call's delta.

In code, calls and puts share one formula through a sign $s = +1$ (call) or $-1$
(put):

$$V = s\left[S e^{-qT} N(s\,d_1) - K e^{-rT} N(s\,d_2)\right]$$

### Greeks

With $\varphi$ the standard normal PDF:

| Greek | Formula                                                                                           | Meaning                                   |
| ----- | ------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| Delta | $s\,e^{-qT} N(s\,d_1)$                                                                            | Price change per \$1 move in spot         |
| Gamma | $\dfrac{e^{-qT}\varphi(d_1)}{S\sigma\sqrt{T}}$                                                    | Change in delta per \$1 move in spot      |
| Vega  | $S e^{-qT}\varphi(d_1)\sqrt{T}$                                                                   | Price change per 1 point of volatility    |
| Theta | $-\dfrac{S e^{-qT}\varphi(d_1)\sigma}{2\sqrt{T}} - s\,rKe^{-rT}N(s\,d_2) + s\,qSe^{-qT}N(s\,d_1)$ | Price change per day                      |
| Rho   | $s\,KTe^{-rT}N(s\,d_2)$                                                                           | Price change per 1 point of interest rate |

### Implied volatility

There is no closed form for $\sigma$ given a price, so it is found numerically.
Newton-Raphson uses vega as the derivative and converges in a few steps near the
money. Every step also keeps a bracket known to contain the answer, and falls
back to bisection when a Newton step would leave it, which guarantees
convergence for deep in- or out-of-the-money options where vega is tiny. Prices
outside the no-arbitrage range are rejected, since no volatility can produce
them.

</details>

## Use as a library

Install from PyPI:

```bash
pip install finn-bs-pricer
```

Then:

```python
from bs_pricer import bs_greeks, bs_price, implied_vol

bs_price(100, 100, 1, 0.05, 0.2, option_type="call")   # 10.4506
bs_greeks(100, 100, 1, 0.05, 0.2, option_type="call")  # {"delta": 0.6368, ...}
implied_vol(10.4506, 100, 100, 1, 0.05)                # 0.2000

# Arrays broadcast: a 2 x 3 grid of prices in one call
import numpy as np
bs_price(np.array([90, 100, 110]), 100, 1, 0.05, np.array([[0.1], [0.2]]))
```

The package installs as `finn-bs-pricer` and imports as `bs_pricer`.

## Run locally

```bash
git clone https://github.com/FinnBrennan/black-scholes-pricer.git
cd black-scholes-pricer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Run the tests:

```bash
pip install pytest
python3 -m pytest
```

## Project structure

```
black-scholes-pricer/
├── bs_pricer/          pricing engine (with no UI dependencies)
│   ├── pricer.py       bs_price, prob_itm, shared input validation
│   ├── greeks.py       bs_greeks
│   └── iv.py           implied_vol
├── tests/              pytest suite for bs_pricer
├── app.py              Streamlit front end
├── charts.py           Plotly sensitivity and Greek charts
├── heatmap.py          Plotly price heatmaps
└── requirements.txt
```

## v1 to v2: Learnings and Changes

I built
[v1](https://github.com/FinnBrennan/black-scholes-pricer/releases/tag/v1.0) in
June of 2026 as one of my first personal projects. Re-approaching the project 5
months later, I have learnt a lot more about Python as well as the maths behind
Black-Scholes. Thus I noticed significant ways in which I would change how I
approached the project, so version 2 has become a complete rewrite rather than a
patch or a few small changes. I have also extended the scope to include Greeks
and Implied Volatility.

- **Actually understanding the maths rather than just the formula.** In v1 I
  implemented Black-Scholes mainly by just copying the formula. For v2 I
  properly understood what each term means and how they interact: $N(d_2)$ as
  the risk-neutral probability of finishing in the money, why
  $d_2 = d_1 - \sigma\sqrt{T}$, and how the Greeks fall out of the same terms.
  That is what made adding Greeks and implied volatility straightforward.
- **Streamlit's execution model.** v1 fought Streamlit with Calculate and Reset
  buttons and a session-state flag to keep results on screen between reruns.
  Once I understood that Streamlit reruns the whole script on every input
  change, all of that could be removed: prices now update live, and `app.py`
  went from 440 lines to 189.
- **Separating the engine from the UI.** Inputs were only validated in the app
  rather than the engine, and my chart functions took 13 arguments. The pricing
  code is now its own package, validates its own inputs, and works on NumPy
  arrays, so charts and heatmaps are single broadcast calls instead of slow and
  messy nested loops.
- **Testing properly.** v1 only had one test checking one value. v2 tests
  against properties that must hold, such as put-call parity and Greeks agreeing
  with bump-and-reprice finite differences, which catch mistakes that the
  previous version wouldn't.
- **Interactive charts.** Static Matplotlib images were replaced with Plotly
  charts and heatmaps you can hover, zoom and pan.
- **New features:** all five Greeks, an implied volatility solver, and a
  Greek-vs-spot chart for each Greek.

More in-depth details of my changes are in [CHANGELOG.md](CHANGELOG.md).

## Acknowledgements

My UI design was inspired by the site: [testfol.io](https://testfol.io). I used
claude for the latex code used in the maths section of this readme.
