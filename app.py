import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm

from pricer import black_scholes
from charts import call_put_stock_chart
from charts import call_put_vol_chart
from charts import options_vs_xaxis


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
    unsafe_allow_html=True
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
    unsafe_allow_html=True
)



st.title(" Black Scholes Pricer ")

#==============================================================================
#
# Sidebar
#
#==============================================================================
with st.sidebar:

    curr_stk_prc = input_1 = st.number_input("Current Stock Price [ $ ]")
    strike_pr = input_2 = st.number_input("Strike Price [ $ ]")
    time_unt_exp = input_3 = st.number_input("Time Until Expiry [ years ]")
    rsk_free_ir = input_4 = st.number_input("Risk Free Interest Rate"
    " [ e.g. 0.05 = 5% ]")
    sigma_vol = input_5 = st.number_input("Volatility [ e.g. 0.05 = 5% ]" 
    " ")
    q = setdefault0 = st.caption("Default q = 0  [dividend yield % per year ]")


    # #temporary for ease of testing
    # curr_stk_prc = 170
    # strike_pr = 155
    # time_unt_exp = 0.5
    # rsk_free_ir = 0.05
    # sigma_vol = 0.25




    st.markdown("""
        <style>
        .stButton button {
            margin: 0px;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3,1])
    with col1:
        calculate = st.button("Calculate Options Price", use_container_width=True)
        
    with col2:
        reset = st.button("Reset", use_container_width=True)

    if reset:
        st.rerun()



#==============================================================================
#
# Call and Put Price Display
#
#==============================================================================

    if calculate:

        # (call_p, put_p) = black_scholes(curr_stk_prc, strike_pr, time_unt_exp, 
        #               rsk_free_ir, sigma_vol)
        prices = black_scholes(curr_stk_prc, strike_pr, time_unt_exp, 
                    rsk_free_ir, sigma_vol)
        call_p = prices[0]
        put_p = prices[1] 


        with st.container():
            st.markdown('<div class="custom-block-green"></div>', unsafe_allow_html=True)
            st.metric(label ="Call Price",value=f"$ {call_p:.3f}")


        with st.container():
            st.markdown('<div class="custom-block-red"></div>', unsafe_allow_html=True)
            st.metric(label ="Put Price",value=f"$ {put_p:.3f}")


    # Default display
    else:

        with st.container():
            st.markdown('<div class="custom-block-green"></div>', unsafe_allow_html=True)
            st.metric(label ="Call Price",value=f"$")


        with st.container():
            st.markdown('<div class="custom-block-red"></div>', unsafe_allow_html=True)
            st.metric(label ="Put Price",value=f"$")




#==============================================================================
#
# Charts 
#
#==============================================================================
    
# On calculate button - display graphs
if calculate:



    # TODO Update to user input later/slider

    low_multi = 0.75
    high_multi = 1.25
    user_datapoints = 20


    # Chart 1 (Call, Put vs Stock)
    #=============================
    (x_datapoints, important_x) = call_put_stock_chart(low_multi, high_multi, user_datapoints, curr_stk_prc)
    

    # call main function for C%P vs x_variable line graphs.
    c_p_s_chart=options_vs_xaxis(x_datapoints,important_x,low_multi,
                    curr_stk_prc,strike_pr, time_unt_exp, 
                    rsk_free_ir, sigma_vol, call_p, put_p, mode = "stock", x_label = "Stock Price $", title = "Stock Price")



    # Chart 2 (Call, Put vs Volatility)
    #==================================
    (x_datapoints, important_x) = call_put_vol_chart(low_multi, high_multi, user_datapoints, sigma_vol)
    

    # call main function for C%P vs x_variable line graphs.
    c_p_v_chart =  options_vs_xaxis(x_datapoints,important_x,low_multi,
                    curr_stk_prc,strike_pr, time_unt_exp, 
                    rsk_free_ir, sigma_vol, call_p, put_p, mode="vol", x_label = "Volatility [0.5 = 50%]", title = "Volatility")



    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(c_p_s_chart)
        
    with col2:
        st.pyplot(c_p_v_chart)
    





#==============================================================================
#
# Progress Tracking 
#
#==============================================================================
    
# V1= python terminal s
# - Done
#=============================


# V2= streamlit for frontend
# -mvp complete 
# -colour scheme implemented 
# -both options prices to x_variable graphs implemented
#=============================

# To Come:

# V3 = react front end. 





