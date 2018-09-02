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

from buspirate.base import BusPirate


# pylint: disable=C0111,E1101
class BusPirateTest(unittest.TestCase):
    """ Unit Test class """
    @mock.patch('serial.Serial', autospec=True)
    def setUp(self, mock_serial): # pylint: disable=W0613,W0221
        """ Unit Test setup """
        self.bus_pirate = BusPirate("/dev/ttyUSB0")

    def tearDown(self):
        """ Unit Test cleanup """
        pass

    def test_enter(self):
        self.bus_pirate.serial.read.return_value = "BBIO1"
        self.assertEqual(self.bus_pirate.enter(), True)
        self.bus_pirate.serial.write.assert_called_with(0x00)

    def test_mode(self):
        self.bus_pirate.serial.read.return_value = "SPI1"
        self.assertEqual(self.bus_pirate.mode(), "SPI1")
        self.bus_pirate.serial.write.assert_called_with(0x01)

    def test_reset(self):
        self.assertEqual(self.bus_pirate.reset(), None)
        self.bus_pirate.serial.write.assert_called_with(0x0F)

    def test_configure_pins(self):
        self.assertEqual(self.bus_pirate.configure_pins(), None)

    def test_set_pins(self):
        self.assertEqual(self.bus_pirate.set_pins(), None)

    def test_configure_peripherials(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.configure_peripherials(), True)
        self.bus_pirate.serial.write.assert_called_with(0x40|0x00)

    def test_bulk_write(self):
        data = [idx for idx in range(1, 17)]
        self.bus_pirate.serial.read.side_effect = [0x01, data]
        result = self.bus_pirate.bulk_write(16, data)
        self.assertEqual(result, data)
        self.bus_pirate.serial.write.assert_any_call(0x1F)
        self.bus_pirate.serial.write.assert_any_call(data)

    def test_bulk_write_fail(self):
        data = [idx for idx in range(1, 17)]
        self.bus_pirate.serial.read.side_effect = [0x00, data]
        result = self.bus_pirate.bulk_write(16, data)
        self.assertEqual(result, bytes())
        self.bus_pirate.serial.write.assert_called_with(0x1F)

    def test_bulk_write_data_is_none(self):
        data = [idx for idx in range(1, 17)]
        self.bus_pirate.serial.read.side_effect = [0x01, data]
        result = self.bus_pirate.bulk_write(16, None)
        self.assertEqual(result, data)
        self.bus_pirate.serial.write.assert_any_call(0x1F)
        self.bus_pirate.serial.write.assert_any_call(bytes(16))

    def test_bulk_write_count_is_too_small(self):
        with self.assertRaises(ValueError):
            data = [idx for idx in range(1, 17)]
            result = self.bus_pirate.bulk_write(0, data)

    def test_bulk_write_count_is_too_big(self):
        with self.assertRaises(ValueError):
            data = [idx for idx in range(1, 17)]
            result = self.bus_pirate.bulk_write(17, data)

    def test__write_then_read(self):
        data = [idx for idx in range(1, 17)]
        self.bus_pirate.serial.read.return_value = [0x01] + data
        result = self.bus_pirate._write_then_read(command=0x04, write_count=16,
                                                  read_count=len(data), write_data=data)
        self.assertEqual(result, data)
        self.bus_pirate.serial.write.assert_called_with([0x04, 16, len(data), data])

    def test__write_then_read_fail(self):
        data = [idx for idx in range(1, 17)]
        self.bus_pirate.serial.read.return_value = [0x00] + data
        result = self.bus_pirate._write_then_read(command=0x04, write_count=16,
                                                  read_count=len(data), write_data=data)
        self.assertEqual(result, bytes())
        self.bus_pirate.serial.write.assert_called_with([0x04, 16, len(data), data])
