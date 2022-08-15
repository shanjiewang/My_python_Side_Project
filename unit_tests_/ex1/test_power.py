
"""
Test module for power.py
"""

import unittest
from power import power_num

class TestPower(unittest.TestCase):
    def test_power_int(self):
        self.assertEqual(power_num(2,3),8)
    def test_power_float(self):
        self.assertEqual(power_num(1.5,2),2.25)

if __name__ == '__main__':
    unittest.main()