import numpy as np
import pytest

from bs_pricer import bs_price

# Reference case: S=100, K=100, T=1, r=5%, sigma=20% (Hull textbook example)
ATM = dict(spot=100, strike=100, expiry=1, rate=0.05, vol=0.2)


def test_atm_call_reference():
    assert bs_price(**ATM, option_type="call") == pytest.approx(10.4506, abs=1e-4)


def test_atm_put_reference():
    assert bs_price(**ATM, option_type="put") == pytest.approx(5.5735, abs=1e-4)


def test_original_v1_values():
    args = (150, 155, 0.5, 0.05, 0.25)
    assert bs_price(*args, option_type="call") == pytest.approx(10.030, abs=1e-3)
    assert bs_price(*args, option_type="put") == pytest.approx(11.203, abs=1e-3)


@pytest.mark.parametrize("div_yield", [0.0, 0.03])
def test_put_call_parity(div_yield):
    # C - P = S*e^(-qT) - K*e^(-rT)
    s, k, t, r = 120, 100, 0.75, 0.04
    call = bs_price(s, k, t, r, 0.3, div_yield, option_type="call")
    put = bs_price(s, k, t, r, 0.3, div_yield, option_type="put")
    expected = s * np.exp(-div_yield * t) - k * np.exp(-r * t)
    assert call - put == pytest.approx(expected)


def test_vectorised_matches_scalar():
    spots = np.array([80.0, 100.0, 120.0])
    vec = bs_price(spots, 100, 1, 0.05, 0.2, option_type="call")
    scalar = [bs_price(s, 100, 1, 0.05, 0.2, option_type="call") for s in spots]
    np.testing.assert_allclose(vec, scalar)


def test_broadcasting_grid_shape():
    spots = np.array([90.0, 100.0, 110.0])  # shape (3,)
    vols = np.array([0.1, 0.2])[:, None]  # shape (2, 1)
    grid = bs_price(spots, 100, 1, 0.05, vols, option_type="call")
    assert grid.shape == (2, 3)


def test_call_increases_with_spot():
    prices = bs_price(np.linspace(50, 150, 20), 100, 1, 0.05, 0.2, option_type="call")
    assert np.all(np.diff(prices) > 0)


@pytest.mark.parametrize(
    "bad",
    [
        dict(spot=0),
        dict(spot=-1),
        dict(strike=0),
        dict(expiry=0),
        dict(vol=0),
        dict(vol=-0.2),
    ],
)
def test_invalid_inputs_raise(bad):
    with pytest.raises(ValueError):
        bs_price(**{**ATM, **bad})


def test_invalid_option_type_raises():
    with pytest.raises(ValueError):
        bs_price(**ATM, option_type="straddle")


def test_prob_itm_call_and_put_sum_to_one():
    from bs_pricer import prob_itm

    call = prob_itm(**ATM, option_type="call")
    put = prob_itm(**ATM, option_type="put")
    assert call + put == pytest.approx(1.0)
