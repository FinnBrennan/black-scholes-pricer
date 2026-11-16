# Changelog

## v2.0 (November 2026)

Version 2 is a complete rebuild of v1. Below documents each change that I have
made as a result of problems in Version 1 and discusses how the current version
solves them.

**Engine**

- **Pricing logic was not separated correctly from the UI.** Moved all logic
  into a standalone `bs_pricer` package that the app imports, so the maths can
  be tested and reused completely separated from Streamlit.
- **Every chart and heatmap priced point by point in Python loops.** All engine
  functions now accept NumPy arrays and broadcast them, so a full heatmap is a
  single call rather than a messy convoluted nested loop.
- **Separate code paths for calls and puts, and d2 recalculated from scratch.**
  d2 is now derived from d1 and both calls and puts are now calculated from 1
  formula in 1 function by using a + or - 1 parameter.
- **Input validation existed only in the Streamlit app, rather than the
  engine.** The engine validates its own inputs in one shared helper function
  and raises a `ValueError`; the app now just catches it rather than performing
  its own input validation.
- **Dividend yield was set to zero as a hard-coded int.** A simple change but
  with my new rewrite of the project it is now treated as an input variable
  throughout the application.
- **New: analytical Greeks** (`bs_greeks`), in trader units.
- **New: implied volatility** (`implied_vol`). Newton-Raphson converges fast but
  can fail when vega is tiny, so each step is kept inside a bracket with a
  bisection fallback, which guarantees convergence. Prices outside no-arbitrage
  bounds are rejected up front through validation.
- **New: probability of finishing in the money** (`prob_itm`).

**App**

- **Calculate and Reset buttons along with session-state flag.** These were
  there to work around Streamlit reruns. I have since understood that Streamlit
  reruns the whole script on every input change therefore making these features
  unnecessary: prices now update live in the application.
- **Five near-identical chart blocks and a 13-argument chart function.** My code
  for charts was a mess of redundant code with a lot of duplicated code. Inputs
  and charts are now handled by small configuration lists and a single `params`
  dict, allowing me to reduce `app.py` from 440 lines to 189.
- **Static Matplotlib and Seaborn images.** I replaced these with interactive
  Plotly charts and heatmaps which was a new library I have got familiar with
  over the last few months. This allows for dynamic zooming and panning as well
  as other features.
- **Redesigned layout.** I built out a fresh UI with a much cleaner design and
  layout. The layout was redesigned with Pricer, Greeks, Implied vol, Heatmaps
  and About sections/tabs, a results table showing price, all Greeks and P(ITM),
  and a live put-call parity check.

**Testing and tooling**

- **One test checking one value.** I previously only had 1 test and I have
  replaced this by a pytest suite built on properties that must always hold:
  put-call parity, Greeks matching bump-and-reprice finite differences, call/put
  Greek relationships, and implied-vol round trips, plus reference values and
  invalid-input cases.

- Lastly I formatted and linted with ruff; dependencies pinned.

## v1.0 (June 2026)

The original version consisted of: (Coded in the following stages):

- **v1.5:** percentage or decimal input toggle; chart datapoint functions merged
  into one; first unit test; call and put heatmaps across spot and volatility
- **v1.4:** input validation and error handling; persistent state so charts
  update live as bounds change; bound sliders
- **v1.3:** the remaining three single-variable charts; adjustable lower and
  upper bounds; charts moved into expanders
- **v1.2:** restyled UI; call and put price against stock price and volatility
  charts; Streamlit theme config
- **v1.1:** Black-Scholes pricer with a simple Streamlit UI
