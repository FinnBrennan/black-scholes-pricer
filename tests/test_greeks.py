import numpy as np
import pytest

from bs_pricer import bs_greeks, bs_price

ATM = {"spot": 100, "strike": 100, "expiry": 1, "rate": 0.05, "vol": 0.2}
# An off-the-money case with a dividend, to exercise every term
CASE = {
    "spot": 110,
    "strike": 100,
    "expiry": 0.75,
    "rate": 0.04,
    "vol": 0.3,
    "div_yield": 0.02,
}


def test_atm_reference_values():
    call = bs_greeks(**ATM, option_type="call")
    put = bs_greeks(**ATM, option_type="put")
    assert call["delta"] == pytest.approx(0.6368, abs=1e-4)
    assert put["delta"] == pytest.approx(-0.3632, abs=1e-4)
    assert call["gamma"] == pytest.approx(0.0188, abs=1e-4)
    assert call["vega"] == pytest.approx(0.3752, abs=1e-4)
    assert call["theta"] == pytest.approx(-0.0176, abs=1e-4)
    assert put["theta"] == pytest.approx(-0.0045, abs=1e-4)
    assert call["rho"] == pytest.approx(0.5323, abs=1e-4)
    assert put["rho"] == pytest.approx(-0.4189, abs=1e-4)


def _bump(param, h, option_type):
    """Central finite difference of bs_price with respect to one input."""
    up = {**CASE, param: CASE[param] + h}
    down = {**CASE, param: CASE[param] - h}
    return (
        bs_price(**up, option_type=option_type)
        - bs_price(**down, option_type=option_type)
    ) / (2 * h)


@pytest.mark.parametrize("option_type", ["call", "put"])
def test_greeks_match_bump_and_reprice(option_type):
    g = bs_greeks(**CASE, option_type=option_type)
    h = 1e-4
    assert g["delta"] == pytest.approx(_bump("spot", h, option_type), rel=1e-5)
    assert g["vega"] == pytest.approx(_bump("vol", h, option_type) / 100, rel=1e-5)
    assert g["rho"] == pytest.approx(_bump("rate", h, option_type) / 100, rel=1e-5)
    # theta is the price change as time passes, i.e. minus the expiry derivative
    assert g["theta"] == pytest.approx(-_bump("expiry", h, option_type) / 365, rel=1e-5)

    # gamma: second difference in spot
    s, hs = CASE["spot"], 1e-2

    def price(spot):
        return bs_price(**{**CASE, "spot": spot}, option_type=option_type)

    gamma_fd = (price(s + hs) - 2 * price(s) + price(s - hs)) / hs**2
    assert g["gamma"] == pytest.approx(gamma_fd, rel=1e-4)


def test_call_put_relationships():
    call = bs_greeks(**CASE, option_type="call")
    put = bs_greeks(**CASE, option_type="put")
    q, t = CASE["div_yield"], CASE["expiry"]
    assert call["delta"] - put["delta"] == pytest.approx(np.exp(-q * t))
    assert call["gamma"] == pytest.approx(put["gamma"])
    assert call["vega"] == pytest.approx(put["vega"])


def test_vectorised():
    spots = np.array([90.0, 100.0, 110.0])
    g = bs_greeks(spots, 100, 1, 0.05, 0.2, option_type="call")
    assert g["delta"].shape == (3,)
    assert np.all(np.diff(g["delta"]) > 0)  # call delta rises with spot


def test_invalid_inputs_raise():
    with pytest.raises(ValueError):
        bs_greeks(**{**ATM, "vol": 0})
    with pytest.raises(ValueError):
        bs_greeks(**ATM, option_type="straddle")
