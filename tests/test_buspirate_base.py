"""
Unit Tests for BusPirate class
"""

import unittest
import unittest.mock as mock
import dummyserial
from buspirate.base import BusPirate

ds_responses = {
        0x00: 'BBIO1',
        0x0F: 0x01,
}

class BusPirateTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch("serial.Serial")
    def test_enter(self, enter):
        self.assertEqual(enter(), "BBIO1")
