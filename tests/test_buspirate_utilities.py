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
Unit Tests for BusPirate base class
"""
import unittest
from unittest import mock

from buspirate.utilities import Voltage, SelfTests, PWM, Frequency


# pylint: disable=C0111,E1101
class BusPirateVoltageTest(unittest.TestCase):
    """ Unit Test class """
    @mock.patch('serial.Serial', autospec=True)
    def setUp(self, mock_serial): # pylint: disable=W0613,W0221
        """ Unit Test setup """
        self.bus_pirate = Voltage("/dev/ttyUSB0")

    def tearDown(self):
        """ Unit Test cleanup """
        pass

    def test_take_once(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.take_once(), True)
        self.bus_pirate.serial.write.assert_called_with(0x14)

    def test_continuous(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.continuous(), True)
        self.bus_pirate.serial.write.assert_called_with(0x15)


class BusPirateSelfTestsTest(unittest.TestCase):
    """ Unit Test class """
    @mock.patch('serial.Serial', autospec=True)
    def setUp(self, mock_serial): # pylint: disable=W0613,W0221
        """ Unit Test setup """
        self.bus_pirate = SelfTests("/dev/ttyUSB0")

    def tearDown(self):
        """ Unit Test cleanup """
        pass

    def test_short_test(self):
        self.assertEqual(self.bus_pirate.short_test(), None)
        self.bus_pirate.serial.write.assert_called_with(0x10)

    def test_long_test(self):
        self.assertEqual(self.bus_pirate.long_test(), None)
        self.bus_pirate.serial.write.assert_called_with(0x11)

    def test_exit(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.exit(), True)
        self.bus_pirate.serial.write.assert_called_with(0xFF)


class BusPiratePWMTest(unittest.TestCase):
    """ Unit Test class """
    @mock.patch('serial.Serial', autospec=True)
    def setUp(self, mock_serial): # pylint: disable=W0613,W0221
        """ Unit Test setup """
        self.bus_pirate = PWM("/dev/ttyUSB0")

    def tearDown(self):
        """ Unit Test cleanup """
        pass

    def test_setup(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.setup(), True)
        self.bus_pirate.serial.write.assert_called_with(0x12)

    def test_clear(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.clear(), True)
        self.bus_pirate.serial.write.assert_called_with(0x13)

    def test_disable(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.disable(), True)
        self.bus_pirate.serial.write.assert_called_with(0x13)


class BusPirateFrequencyTest(unittest.TestCase):
    """ Unit Test class """
    @mock.patch('serial.Serial', autospec=True)
    def setUp(self, mock_serial): # pylint: disable=W0613,W0221
        """ Unit Test setup """
        self.bus_pirate = Frequency("/dev/ttyUSB0")

    def tearDown(self):
        """ Unit Test cleanup """
        pass

    def test_measure(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.measure(), True)
        self.bus_pirate.serial.write.assert_called_with(0x16)
