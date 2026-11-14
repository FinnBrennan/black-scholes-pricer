"""Option price sensitivity charts."""

import numpy as np
import plotly.graph_objects as go

from bs_pricer import bs_price

CALL_COLOUR = "#00B32C"
PUT_COLOUR = "#B3000C"


def sweep(base, low_mult, high_mult, n_points):
    """Evenly spaced values from low_mult * base to high_mult * base."""
    return np.linspace(low_mult * base, high_mult * base, n_points)


def sensitivity_chart(params, vary, x_values, label):
    """
    Call and put price as one input varies, all others held fixed.

    params : dict with keys spot, strike, expiry, rate, vol, div_yield
    vary : which key in params to sweep
    x_values : array of values for that input
    label : axis label for the varied input
    """
    swept = {**params, vary: x_values}
    calls = bs_price(**swept, option_type="call")
    puts = bs_price(**swept, option_type="put")

    current = params[vary]
    call_now = bs_price(**params, option_type="call")
    put_now = bs_price(**params, option_type="put")

    fig = go.Figure()
    fig.add_scatter(x=x_values, y=calls, name="Call", line={"color": CALL_COLOUR})
    fig.add_scatter(x=x_values, y=puts, name="Put", line={"color": PUT_COLOUR})
    fig.add_vline(x=current, line_dash="dash", line_color="grey")
    fig.add_scatter(
        x=[current, current],
        y=[call_now, put_now],
        mode="markers",
        marker={"color": [CALL_COLOUR, PUT_COLOUR], "size": 9},
        showlegend=False,
        hoverinfo="skip",
    )
    fig.update_layout(
        title=f"Option price vs {label}",
        xaxis_title=label,
        yaxis_title="Option price ($)",
        hovermode="x unified",
    )
    return fig
