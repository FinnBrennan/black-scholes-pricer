"""Black-Scholes pricing engine for European options"""

import numpy as np
from scipy.stats import norm


def _d1_d2(spot, strike, expiry, rate, vol, div_yield):
    """Black-Scholes formula d1 and d2 term calcuations."""
    vol_sqrt_t = vol * np.sqrt(expiry)
    d1 = (
        np.log(spot / strike) + (rate - div_yield + 0.5 * vol**2) * expiry
    ) / vol_sqrt_t
    d2 = d1 - vol_sqrt_t
    return d1, d2


def bs_price(spot, strike, expiry, rate, vol, div_yield=0.0, option_type="call"):
    """
    Black-Scholes price (European option)

    Parameters
    ----------
    spot : current underlying price (S)
    strike : strike price (K)
    expiry : time to expiry in years (T)
    rate : continuously compounded risk-free rate (r)
    vol : annualised volatility (σ)
    div_yield : continuous dividend yield (q), default 0
    option_type : "call" or "put"

    All numeric inputs can accept scalars or NumPy arrays
    (Inputs are now broadcast together).

    price = phi · [S·e^(-qT)·N(phi·d1) - K·e^(-rT)·N(phi·d2)],  phi = +1 call, -1 put
    """
    spot, strike, expiry, rate, vol, div_yield = (
        np.asarray(x, dtype=float) for x in (spot, strike, expiry, rate, vol, div_yield)
    )

    if option_type not in ("call", "put"):
        raise ValueError(f"option_type must be 'call' or 'put', got {option_type!r}")
    if (
        np.any(spot <= 0)
        or np.any(strike <= 0)
        or np.any(expiry <= 0)
        or np.any(vol <= 0)
    ):
        raise ValueError("spot, strike, expiry and vol must all be positive")

    phi = 1.0 if option_type == "call" else -1.0
    d1, d2 = _d1_d2(spot, strike, expiry, rate, vol, div_yield)

    return phi * (
        spot * np.exp(-div_yield * expiry) * norm.cdf(phi * d1)
        - strike * np.exp(-rate * expiry) * norm.cdf(phi * d2)
    )
