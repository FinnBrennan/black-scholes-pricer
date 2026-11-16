"""Streamlit front end for the Black-Scholes pricer. UI inspired by testfol.io."""

import numpy as np
import streamlit as st

from bs_pricer import bs_price, prob_itm, implied_vol, bs_greeks
from charts import sensitivity_chart, sweep, GREEK_LABELS, greek_chart
from heatmap import price_heatmap

st.set_page_config(page_title="Black-Scholes Options Pricer", layout="wide")

# (key in params, input label, default, step, is_percent)
INPUTS = [
    ("spot", "Spot price ($)", 100.0, 1.0, False),
    ("strike", "Strike price ($)", 100.0, 1.0, False),
    ("expiry", "Time to expiry (years)", 1.0, 0.25, False),
    ("rate", "Risk-free rate (%)", 5.0, 0.25, True),
    ("vol", "Volatility (%)", 20.0, 1.0, True),
    ("div_yield", "Dividend yield (%)", 0.0, 0.25, True),
]

# (key in params, chart axis label)
SWEEPS = [
    ("spot", "Spot price ($)"),
    ("strike", "Strike price ($)"),
    ("expiry", "Time to expiry (years)"),
    ("rate", "Risk-free rate (decimal)"),
    ("vol", "Volatility (decimal)"),
    ("div_yield", "Dividend yield (decimal)"),
]

st.title("Black-Scholes Options Pricer")
section = (
    st.segmented_control(
        "Section",
        ["Pricer", "Greeks", "Implied vol", "Heatmaps", "About"],
        default="Pricer",
        label_visibility="collapsed",
    )
    or "Pricer"
)  # clicking the active button deselects it; fall back to Pricer

# Parameters
# ----------------------------------------------------------------
with st.container(border=True):
    st.subheader("Parameters")
    params = {}
    for col, (key, label, default, step, is_percent) in zip(
        st.columns(len(INPUTS)), INPUTS
    ):
        value = col.number_input(label, value=default, step=step, format="%.2f")
        params[key] = value / 100 if is_percent else value

    low, high = st.slider(
        "Chart range (multiple of current value)", 0.1, 2.0, (0.75, 1.25), 0.05
    )

try:
    call = float(bs_price(**params, option_type="call"))
    put = float(bs_price(**params, option_type="put"))
except ValueError as err:
    st.error(f"Invalid inputs: {err}")
    st.stop()

# Pricer
# ----------------------------------------------------------------
if section == "Pricer":
    with st.container(border=True):
        st.subheader("Results")
        rows = []
        for option_type, price in [("call", call), ("put", put)]:
            greeks = bs_greeks(**params, option_type=option_type)
            rows.append(
                {
                    "Option": option_type.title(),
                    "Price": price,
                    "Delta": float(greeks["delta"]),
                    "Gamma": float(greeks["gamma"]),
                    "Vega (1%)": float(greeks["vega"]),
                    "Theta (day)": float(greeks["theta"]),
                    "Rho (1%)": float(greeks["rho"]),
                    "P(ITM)": float(prob_itm(**params, option_type=option_type)),
                }
            )
        st.dataframe(
            rows,
            hide_index=True,
            width="stretch",
            column_config={
                col: st.column_config.NumberColumn(format="%.4f")
                for col in rows[0]
                if col not in ("Option", "P(ITM)")
            }
            | {"P(ITM)": st.column_config.NumberColumn(format="percent")},
        )

        S, K, T = params["spot"], params["strike"], params["expiry"]
        parity = S * np.exp(-params["div_yield"] * T) - K * np.exp(-params["rate"] * T)
        st.caption(
            f"Put-call parity: $C - P = {call - put:.4f}$, "
            f"$Se^{{-qT}} - Ke^{{-rT}} = {parity:.4f}$"
        )

    with st.container(border=True):
        st.subheader("Sensitivity")
        labels = dict(SWEEPS)
        vary = st.selectbox("Vary", list(labels), format_func=labels.get)
        n_points = 100

        base = params[vary]
        if base == 0:
            # A multiple of zero is zero, so sweep a fixed range instead.
            x_values = np.linspace(0.0, 0.10, n_points)
        else:
            x_values = sweep(base, low, high, n_points)

        st.plotly_chart(
            sensitivity_chart(params, vary, x_values, labels[vary]), width="stretch"
        )


# Greeks
# ----------------------------------------------------------------
elif section == "Greeks":
    st.caption(
        "Each Greek as spot varies, all other inputs fixed. Dashed line marks current spot."
    )
    spots = sweep(params["spot"], low, high, 100)
    cols = st.columns(2)
    for i, greek in enumerate(GREEK_LABELS):
        with cols[i % 2], st.container(border=True):
            st.plotly_chart(greek_chart(params, greek, spots), width="stretch")


# Implied vol
# ----------------------------------------------------------------
elif section == "Implied vol":
    with st.container(border=True):
        st.subheader("Implied volatility")
        st.caption(
            "Enter a market price to find the volatility the market is implying. "
            "Uses every input above except volatility."
        )
        left, right = st.columns(2)
        iv_type = left.radio("Option", ["Call", "Put"], horizontal=True)
        model_price = call if iv_type == "Call" else put
        market_price = right.number_input(
            "Market price ($)",
            value=round(model_price, 2),
            step=0.10,
            format="%.2f",
            key=f"market_price_{iv_type}",
        )
        iv_args = {k: v for k, v in params.items() if k != "vol"}
        try:
            iv = implied_vol(market_price, **iv_args, option_type=iv_type.lower())
            st.metric("Implied volatility", f"{iv:.2%}")
        except (ValueError, RuntimeError) as err:
            st.warning(str(err))


# Heatmaps
# ----------------------------------------------------------------
elif section == "Heatmaps":
    spots = sweep(params["spot"], low, high, 10)
    vols = sweep(params["vol"], low, high, 10)
    left, right = st.columns(2)
    with left, st.container(border=True):
        st.plotly_chart(price_heatmap(params, spots, vols, "call"), width="stretch")
    with right, st.container(border=True):
        st.plotly_chart(price_heatmap(params, spots, vols, "put"), width="stretch")


# About
# ----------------------------------------------------------------
else:
    with st.container(border=True):
        st.subheader("About")
        st.markdown("""
Prices European options with the Black-Scholes model, including a continuous dividend yield.

**Features:** call and put prices, all five Greeks, implied volatility from a market price,
sensitivity charts and price heatmaps.

**Assumptions:** constant volatility and interest rate, lognormal stock prices,
no transaction costs, exercise only at expiry.

**Built by Finn Brennan** · [Source and tests on GitHub](https://github.com/FinnBrennan/black-scholes-pricer)
""")
