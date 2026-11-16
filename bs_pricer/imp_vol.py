"""Implied volatility: invert the Black-Scholes formula for vol."""

import numpy as np
from scipy.stats import norm

from .pricer import _d1_d2, bs_price

VOL_LOW = 1e-6
VOL_HIGH = 5.0  # 500% vol: a wide bracket that any sane market price falls inside


def implied_vol(
    price,
    spot,
    strike,
    expiry,
    rate,
    div_yield=0.0,
    option_type="call",
    tol=1e-8,
    max_iter=100,
):
    """
    Volatility that makes the Black-Scholes price equal a given market price.

    Newton-Raphson using vega, safeguarded by bisection: every step keeps a
    bracket [low, high] known to contain the answer, and falls back to the
    bracket midpoint whenever a Newton step would leave it or vega is too small
    to trust. Newton converges in a handful of steps near the money; bisection
    guarantees convergence everywhere else.

    Scalar inputs only. Raises ValueError if the price breaks no-arbitrage bounds
    (no volatility can produce it) and RuntimeError if it fails to converge.
    """
    if option_type not in ("call", "put"):
        raise ValueError(f"option_type must be 'call' or 'put', got {option_type!r}")
    if spot <= 0 or strike <= 0 or expiry <= 0:
        raise ValueError("spot, strike and expiry must all be positive")

    # No-arbitrage bounds: price must lie strictly between intrinsic value
    # (vol -> 0) and the discounted underlying or strike (vol -> infinity).
    disc_spot = spot * np.exp(-div_yield * expiry)
    pv_strike = strike * np.exp(-rate * expiry)
    if option_type == "call":
        lower, upper = max(disc_spot - pv_strike, 0.0), disc_spot
    else:
        lower, upper = max(pv_strike - disc_spot, 0.0), pv_strike
    if not lower < price < upper:
        raise ValueError(
            f"price {price} is outside the no-arbitrage range ({lower:.4f}, {upper:.4f})"
        )

    low, high = VOL_LOW, VOL_HIGH
    vol = 0.2  # starting guess
    for _ in range(max_iter):
        diff = (
            float(bs_price(spot, strike, expiry, rate, vol, div_yield, option_type))
            - price
        )
        if abs(diff) < tol:
            return vol

        # Price rises with vol, so the sign of diff says which side the answer is on.
        if diff > 0:
            high = vol
        else:
            low = vol

        d1, _ = _d1_d2(spot, strike, expiry, rate, vol, div_yield)
        vega = disc_spot * norm.pdf(d1) * np.sqrt(expiry)  # raw vega, per 1.00 of vol

        newton = vol - diff / vega if vega > 1e-12 else np.nan
        vol = newton if low < newton < high else 0.5 * (low + high)

    raise RuntimeError(f"implied vol did not converge in {max_iter} iterations")
