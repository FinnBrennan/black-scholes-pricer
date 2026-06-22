import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pricer import black_scholes

import unittest


class TestBlackScholes(unittest.TestCase):

    def test_decimal_inputs(self):
        call_p, put_p = black_scholes(150, 155, 0.5, 0.05, 0.25)
        self.assertAlmostEqual(call_p, 10.030, places=2)
        self.assertAlmostEqual(put_p, 11.203, places=2)


if __name__ == "__main__":
    unittest.main()
