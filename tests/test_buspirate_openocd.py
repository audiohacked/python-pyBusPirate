# Created by Sean Nelson on 2018-08-19.
# Copyright 2018 Sean Nelson <audiohacked@gmail.com>
#
# This file is part of pyBusPirate.
#
# pyBusPirate is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# pyBusPirate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyBusPirate.  If not, see <https://www.gnu.org/licenses/>.

"""
Unit Tests for BusPirate SPI class
"""
import unittest
from unittest import mock

from buspirate import openocd


# pylint: disable=C0111,E1101
class BusPirateOpenOCDTest(unittest.TestCase):
    @mock.patch('serial.Serial', autospec=True)
    def setUp(self, mock_serial):  # pylint: disable=W0613,W0221
        self.bus_pirate = openocd.JTAG("/dev/ttyUSB0")

    def tearDown(self):
        pass

    def test_exit(self):
        self.bus_pirate.serial.read.return_value = "BBIO1"
        self.assertEqual(self.bus_pirate.exit, True)
        self.bus_pirate.serial.write.assert_called_with(0x00)

    def test_mode(self):
        self.bus_pirate.serial.read.return_value = "1W01"
        self.assertEqual(self.bus_pirate.mode, "1W01")
        self.bus_pirate.serial.write.assert_called_with(0x01)

    def test_enter(self):
        self.bus_pirate.serial.read.return_value = "1W01"
        self.assertEqual(self.bus_pirate.enter, True)
        self.bus_pirate.serial.write.assert_called_with(0x06)
