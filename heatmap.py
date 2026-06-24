import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pricer import black_scholes


def main_heatmap(
    stock_price_datapoints,
    vol_datapoints,
    call_or_put,
    strike_pr,
    time_unt_exp,
    rsk_free_ir,
):

    call_or_put_datapoints = options2d(
        stock_price_datapoints,
        vol_datapoints,
        call_or_put,
        strike_pr,
        time_unt_exp,
        rsk_free_ir,
    )

    fig = heatmap_plotting(
        stock_price_datapoints, vol_datapoints, call_or_put_datapoints, call_or_put
    )
    return fig


def options2d(
    stock_price_datapoints,
    vol_datapoints,
    call_or_put,
    strike_pr,
    time_unt_exp,
    rsk_free_ir,
):
    """Generates a 2d array of z points (call or put prices) for heatmaps."""

    if call_or_put == "call":
        bs_res_index = 0
    else:
        bs_res_index = 1

    z_2darray = np.zeros((len(vol_datapoints), len(stock_price_datapoints)))

    for i, vol in enumerate(vol_datapoints):
        for j, s in enumerate(stock_price_datapoints):
            prices = black_scholes(s, strike_pr, time_unt_exp, rsk_free_ir, vol)
            z_2darray[i, j] = prices[bs_res_index]

    return z_2darray


# Creates a heatmap with stock price on x, volatility on y, against z = either call or put price


def heatmap_plotting(
    stock_price_datapoints, vol_datapoints, call_or_put_datapoints, call_or_put
):
    """Creates a heatmap with stock price on x, volatility on y, against z = either call or put price"""

    fig, ax = plt.subplots(figsize=(8, 6))

    sns.heatmap(
        call_or_put_datapoints,
        xticklabels=np.round(stock_price_datapoints, 1),
        yticklabels=np.round(vol_datapoints, 3),
        annot=True,
        fmt=".1f",
        cmap="RdYlGn",
        ax=ax,
    )

    if call_or_put == "call":
        title = "Call Price vs Stock Price and Volatility"

    else:
        title = "Put Price vs Stock Price and Volatility"

    plt.title(title)
    plt.xlabel("Stock Price")
    plt.ylabel("Volatility")

    return fig
