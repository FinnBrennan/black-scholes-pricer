import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm

from pricer import black_scholes
from charts import call_put_stock_chart
from charts import call_put_vol_chart
from charts import options_vs_xaxis
from charts import call_put_strike_chart
from charts import call_put_time_chart
from charts import call_put_rate_chart

# Wide screen streamlit:
st.set_page_config(layout="wide")


# For persistent state
if "calculated" not in st.session_state:
    st.session_state.calculated = False


# CSS for call price display (Green box)
st.markdown(
    """
    <style>
    [data-testid="stVerticalBlock"] > div:has(div.custom-block-green) {
        background-color: #00B32c;
        border-radius: 8px;
        padding-left: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# CSS for put price display (Red box)
st.markdown(
    """
    <style>
    [data-testid="stVerticalBlock"] > div:has(div.custom-block-red) {
        background-color: #B3000C;
        border-radius: 8px;
        padding-left: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.title(" Black Scholes Pricer ")


# =============================================================================
#
# Sidebar
#
# =============================================================================
with st.sidebar:

    # Input Validation Rules:
    # Stock Price > 0
    # Strike Price > 0
    # Time > 0
    # Interest Rate > 0
    # Volatility > 0

    curr_stk_prc = input_1 = st.number_input("Current Stock Price [ $ ]")
    strike_pr = input_2 = st.number_input("Strike Price [ $ ]")
    time_unt_exp = input_3 = st.number_input("Time Until Expiry [ years ]")
    rsk_free_ir = input_4 = st.number_input(
        "Risk Free Interest Rate" " [ e.g. 0.05 = 5% ]"
    )
    sigma_vol = input_5 = st.number_input("Volatility [ e.g. 0.05 = 5% ]" " ")
    q = setdefault0 = st.caption("Default q = 0  [dividend yield % per year ]")

    # temporary for ease of testing
    # curr_stk_prc = 150
    # strike_pr = 155
    # time_unt_exp = 0.5
    # rsk_free_ir = 0.05
    # sigma_vol = 0.25

    st.markdown(
        """
        <style>
        .stButton button {
            margin: 0px;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        calculate = st.button("Calculate Options Price", use_container_width=True)

    with col2:
        reset = st.button("Reset", use_container_width=True)

    if reset:

        st.session_state.calculated = False
        st.rerun()


# =============================================================================
#
# Call and Put Price Display
#
# =============================================================================

if calculate:
    st.session_state.calculated = True

    # Validate Inputs:
    errors = []

    if curr_stk_prc <= 0:
        errors.append("Stock price must be greater than 0")
    if strike_pr <= 0:
        errors.append("Strike price must be greater than 0")
    if time_unt_exp <= 0:
        errors.append("Time until expiry must be greater than 0")
    if rsk_free_ir <= 0:
        errors.append("Risk free interest rate must be greater than 0")
    if sigma_vol <= 0:
        errors.append("Volatility must be greater than 0")

    if errors:
        for error in errors:
            st.error(error)
        st.stop()

    # (call_p, put_p) = black_scholes(curr_stk_prc, strike_pr, time_unt_exp,
    #               rsk_free_ir, sigma_vol)
    prices = black_scholes(
        curr_stk_prc, strike_pr, time_unt_exp, rsk_free_ir, sigma_vol
    )
    call_p = prices[0]
    put_p = prices[1]

    # Store in current state
    st.session_state.call_p = call_p
    st.session_state.put_p = put_p

if st.session_state.calculated:
    call_p = st.session_state.call_p
    put_p = st.session_state.put_p

    with st.sidebar:

        with st.container():
            st.markdown(
                '<div class="custom-block-green"></div>', unsafe_allow_html=True
            )
            st.metric(label="Call Price", value=f"$ {call_p:.3f}")

        with st.container():
            st.markdown('<div class="custom-block-red"></div>', unsafe_allow_html=True)
            st.metric(label="Put Price", value=f"$ {put_p:.3f}")

    # =========================================================================
    #
    # Charts
    #
    # =========================================================================

    # On calculate button - display graphs

    st.divider()

    st.subheader("Option Price VS Single x-Variable Graphs")
    st.divider()

    col1, col2 = st.columns([1, 5])

    with col1:
        low_multi = st.slider(
            "Lower Bound",
            min_value=0.1,
            max_value=0.99,
            value=0.75,
            step=0.05,
            help="e.g. 0.75 = 25% below current value",
        )

        high_multi = st.slider(
            "Upper Bound",
            min_value=1.01,
            max_value=2.0,
            value=1.25,
            step=0.05,
            help="e.g. 1.25 = 25% above current value",
        )

        user_datapoints = st.slider(
            "# of Datapoints",
            min_value=10,
            max_value=200,
            value=25,
            step=5,
            help="More points = smoother curves",
        )

    # Chart 1 (Call, Put vs Stock)
    # =============================
    x_datapoints, important_x = call_put_stock_chart(
        low_multi, high_multi, user_datapoints, curr_stk_prc
    )

    # call main function for C%P vs x_variable line graphs.
    c_p_s_chart = options_vs_xaxis(
        x_datapoints,
        important_x,
        low_multi,
        curr_stk_prc,
        strike_pr,
        time_unt_exp,
        rsk_free_ir,
        sigma_vol,
        call_p,
        put_p,
        mode="stock",
        x_label="Stock Price $",
        title="Stock Price",
    )

    # Chart 2 (Call, Put vs Volatility)
    # ==================================
    x_datapoints, important_x = call_put_vol_chart(
        low_multi, high_multi, user_datapoints, sigma_vol
    )

    # call main function for C%P vs x_variable line graphs.
    c_p_v_chart = options_vs_xaxis(
        x_datapoints,
        important_x,
        low_multi,
        curr_stk_prc,
        strike_pr,
        time_unt_exp,
        rsk_free_ir,
        sigma_vol,
        call_p,
        put_p,
        mode="vol",
        x_label="Volatility [0.5 = 50%]",
        title="Volatility",
    )

    # Chart 3 (Call, Put vs Strike)
    # ==================================
    x_datapoints, important_x = call_put_strike_chart(
        low_multi, high_multi, user_datapoints, strike_pr
    )

    # call main function for C%P vs x_variable line graphs.
    c_p_strike_chart = options_vs_xaxis(
        x_datapoints,
        important_x,
        low_multi,
        curr_stk_prc,
        strike_pr,
        time_unt_exp,
        rsk_free_ir,
        sigma_vol,
        call_p,
        put_p,
        mode="strike",
        x_label="Strike Price $",
        title="Strike Price",
    )

    # Chart 4 (Call, Put vs Time)
    # ==================================
    x_datapoints, important_x = call_put_time_chart(
        low_multi, high_multi, user_datapoints, time_unt_exp
    )

    # call main function for C%P vs x_variable line graphs.
    c_p_t_chart = options_vs_xaxis(
        x_datapoints,
        important_x,
        low_multi,
        curr_stk_prc,
        strike_pr,
        time_unt_exp,
        rsk_free_ir,
        sigma_vol,
        call_p,
        put_p,
        mode="time",
        x_label="Time Until Expiry [years]",
        title="Time Until Expiry",
    )

    # Chart 5 (Call, Put vs Rate)
    # ==================================
    x_datapoints, important_x = call_put_rate_chart(
        low_multi, high_multi, user_datapoints, time_unt_exp
    )

    # call main function for C%P vs x_variable line graphs.
    c_p_r_chart = options_vs_xaxis(
        x_datapoints,
        important_x,
        low_multi,
        curr_stk_prc,
        strike_pr,
        time_unt_exp,
        rsk_free_ir,
        sigma_vol,
        call_p,
        put_p,
        mode="rate",
        x_label="Risk Free Interest Rate [0.5 = 50%]",
        title="Interest Rate",
    )

    with col2:

        with st.expander("Stock Price"):
            st.pyplot(c_p_s_chart)
        with st.expander("Volatility"):
            st.pyplot(c_p_v_chart)
        with st.expander("Strike Price"):
            st.pyplot(c_p_strike_chart)
        with st.expander("Time Until Expiry"):
            st.pyplot(c_p_t_chart)
        with st.expander("Interest Rate"):
            st.pyplot(c_p_r_chart)


# =============================================================================
#
# Default Display
#
# =============================================================================


# Default display
else:
    with st.sidebar:
        with st.container():
            st.markdown(
                '<div class="custom-block-green"></div>', unsafe_allow_html=True
            )
            st.metric(label="Call Price", value=f"$")

        with st.container():
            st.markdown('<div class="custom-block-red"></div>', unsafe_allow_html=True)
            st.metric(label="Put Price", value=f"$")

    st.subheader("Enter 5 valid inputs to calculate options price")


# =============================================================================
# hello
# Progress Tracking
#
# =============================================================================


# V1= python terminal
# - Done
# =============================


# V2 = Streamlit for frontend + 2 graphs
# -mvp complete
# -colour scheme implemented
# -both options prices to x_variable graphs implemented
# =============================


# V3 = Complete all 5 single variable graphs + Sliders.
# - Completed

# V4 = Persistant State for live graph updates after bound adjustments.
# - Also:
# - Error handling and input validation
# - Bounds now sliders not number input boxes.
# - Slight styling changes


# To Come:

# React front end.
