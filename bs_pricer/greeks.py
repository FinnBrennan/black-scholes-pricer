"""Black-Scholes Greeks for European options."""

import numpy as np
from scipy.stats import norm

from .pricer import _d1_d2, _prepare


def bs_greeks(spot, strike, expiry, rate, vol, div_yield=0.0, option_type="call"):
    """
    Black-Scholes Greeks of a European option.

    Takes the same inputs as bs_price (scalars or NumPy arrays, broadcast together).

    Returns a dict of trader-convention values:
        delta : change in price per $1 move in spot
        gamma : change in delta per $1 move in spot
        vega  : change in price per 1 percentage point rise in vol
        theta : change in price per calendar day (365-day year)
        rho   : change in price per 1 percentage point rise in rate

    With φ the standard normal PDF, N the CDF and sign = +1 call, −1 put:
        delta = sign · e^(−qT) · N(sign·d1)
        gamma = e^(−qT) · φ(d1) / (S·σ·√T)
        vega  = S · e^(−qT) · φ(d1) · √T
        theta = −S·e^(−qT)·φ(d1)·σ / (2√T) − sign·r·K·e^(−rT)·N(sign·d2)
                + sign·q·S·e^(−qT)·N(sign·d1)
        rho   = sign · K · T · e^(−rT) · N(sign·d2)
    (vega, theta and rho are then scaled to the units above.)
    """
    spot, strike, expiry, rate, vol, div_yield, sign = _prepare(
        spot, strike, expiry, rate, vol, div_yield, option_type
    )
    d1, d2 = _d1_d2(spot, strike, expiry, rate, vol, div_yield)

    sqrt_t = np.sqrt(expiry)
    div_disc = np.exp(-div_yield * expiry)
    rate_disc = np.exp(-rate * expiry)
    pdf_d1 = norm.pdf(d1)
    cdf_d1 = norm.cdf(sign * d1)
    cdf_d2 = norm.cdf(sign * d2)

    delta = sign * div_disc * cdf_d1
    gamma = div_disc * pdf_d1 / (spot * vol * sqrt_t)
    vega = spot * div_disc * pdf_d1 * sqrt_t
    theta = (
        -spot * div_disc * pdf_d1 * vol / (2 * sqrt_t)
        - sign * rate * strike * rate_disc * cdf_d2
        + sign * div_yield * spot * div_disc * cdf_d1
    )
    rho = sign * strike * expiry * rate_disc * cdf_d2

    return {
        "delta": delta,
        "gamma": gamma,
        "vega": vega / 100,
        "theta": theta / 365,
        "rho": rho / 100,
    }
