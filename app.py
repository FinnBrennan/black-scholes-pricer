import streamlit as st
import pandas as pd
from pricer import black_scholes
import numpy as np
from scipy.stats import norm

st.title(" --- Black Scholes Pricer --- ")

curr_stk_prc = input_1 = st.number_input("Current Stock Price [ $ ]")
strike_pr = input_2 = st.number_input("Strike Price [ $ ]")
time_unt_exp = input_3 = st.number_input("Time Until Expiry [ years ]")
rsk_free_ir = input_4 = st.number_input("Risk Free Interest Rate"
" [ 0.00 (decimal percentage) ]")
sigma_vol = input_5 = st.number_input("Volatility [ 0.00 (decimal percentage) ]" \
" ")
q = setdefault0 = st.caption("Default q = 0  [dividend yield % per year ]")

calculate = st.button("Calculate Options Price")

if calculate:
  
    # (call_p, put_p) = black_scholes(curr_stk_prc, strike_pr, time_unt_exp, 
    #               rsk_free_ir, sigma_vol)
    prices = black_scholes(curr_stk_prc, strike_pr, time_unt_exp, 
                  rsk_free_ir, sigma_vol)
    call_p = prices[0]
    put_p = prices[1] 

    st.subheader(" --- Call Price ---")
    st.text(f"${call_p:.3f}")

    st.subheader(" --- Put Price ---")
    st.text(f"${put_p:.3f}")
else:



    st.subheader(" --- Call Price ---")
    st.text(f"___")

    st.subheader(" --- Put Price ---")
    st.text(f"___")

    #Front end code here



#streamlist for first iteration. 
# V1= python terminal 
# - Done
# V2= streamlit for frontend
# V3 = react front end. 





