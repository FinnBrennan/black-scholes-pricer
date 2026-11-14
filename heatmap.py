"""Option price heatmaps across spot and volatility."""

import numpy as np
import plotly.graph_objects as go

from bs_pricer import bs_price


def price_grid(params, spots, vols, option_type):
    """Prices on a vol x spot grid (rows = vols, columns = spots) via broadcasting."""
    grid = {**params, "spot": spots[np.newaxis, :], "vol": vols[:, np.newaxis]}
    return bs_price(**grid, option_type=option_type)


def price_heatmap(params, spots, vols, option_type):
    """Heatmap of call or put price against spot (x) and volatility (y)."""
    prices = price_grid(params, spots, vols, option_type)

    fig = go.Figure(
        go.Heatmap(
            z=prices,
            x=np.round(spots, 2),
            y=np.round(vols, 3),
            colorscale="RdYlGn",
            text=np.round(prices, 2),
            texttemplate="%{text}",
            colorbar={"title": "Price ($)"},
        )
    )
    fig.update_layout(
        title=f"{option_type.title()} price vs spot and volatility",
        xaxis_title="Spot price ($)",
        yaxis_title="Volatility",
    )
    return fig
