import numpy as np
import pytest

from bs_pricer import bs_price, implied_vol


@pytest.mark.parametrize("option_type", ["call", "put"])
@pytest.mark.parametrize("strike", [60, 90, 100, 110, 160])
@pytest.mark.parametrize("vol", [0.05, 0.2, 0.6, 1.5])
def test_round_trip(option_type, strike, vol):
    """Price an option at a known vol, then recover that vol from the price."""
    args = {
        "spot": 100,
        "strike": strike,
        "expiry": 0.5,
        "rate": 0.03,
        "div_yield": 0.01,
    }
    price = float(bs_price(**args, vol=vol, option_type=option_type))

    # Time value = price minus its value at zero vol. When it rounds to nothing,
    # every small vol gives the same price, so vol cannot be recovered from it.
    disc_spot = args["spot"] * np.exp(-args["div_yield"] * args["expiry"])
    pv_strike = args["strike"] * np.exp(-args["rate"] * args["expiry"])
    sign = 1 if option_type == "call" else -1
    if price - max(sign * (disc_spot - pv_strike), 0) < 1e-6:
        pytest.skip("no time value: vol is not identifiable from the price")
    assert implied_vol(price, **args, option_type=option_type) == pytest.approx(
        vol, abs=1e-6
    )


def test_reference_value():
    # ATM call worth 10.4506 with S=K=100, T=1, r=5% corresponds to 20% vol
    assert implied_vol(10.450583572185565, 100, 100, 1, 0.05) == pytest.approx(0.2)


@pytest.mark.parametrize(
    ("price", "option_type"),
    [
        (0.0, "call"),  # at or below intrinsic value
        (-1.0, "call"),
        (100.0, "call"),  # at or above the spot price
        (200.0, "put"),  # above the discounted strike
    ],
)
def test_arbitrage_violations_raise(price, option_type):
    with pytest.raises(ValueError):
        implied_vol(price, 100, 100, 1, 0.05, option_type=option_type)


def test_invalid_inputs_raise():
    with pytest.raises(ValueError):
        implied_vol(10, 100, 100, 0, 0.05)
    with pytest.raises(ValueError):
        implied_vol(10, 100, 100, 1, 0.05, option_type="straddle")
