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

from buspirate import onewire


# pylint: disable=C0111,E1101
class BusPirateOneWireTest(unittest.TestCase):
    @mock.patch('serial.Serial', autospec=True)
    def setUp(self, mock_serial): # pylint: disable=W0613,W0221
        self.bus_pirate = onewire.OneWire("/dev/ttyUSB0")

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
        self.bus_pirate.serial.write.assert_called_with(0x04)

    def test_read_byte(self) -> bytes:
        self.bus_pirate.serial.read.side_effect = [0x01, 0xFF]
        self.assertEqual(self.bus_pirate.read_byte(), True)
        self.bus_pirate.serial.write.assert_called_with(0x04)

    def test_rom_search(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.rom_search, True)
        self.bus_pirate.serial.write.assert_called_with(0x08)

    def test_alarm_search(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.alarm_search, True)
        self.bus_pirate.serial.write.assert_called_with(0x09)

    def test_1wire_bulk_write(self):
        read_data = [0x00 for idx in range(1, 17)]
        write_data = [idx for idx in range(1, 17)]
        self.bus_pirate.serial.read.side_effect = [0x01, read_data]
        result = self.bus_pirate.bulk_write(16, write_data)
        self.assertEqual(result, read_data)
        self.bus_pirate.serial.write.assert_any_call(0x1F)
        self.bus_pirate.serial.write.assert_any_call(write_data)

    def test_pullup_voltage_select(self):
        with self.assertRaises(NotImplementedError):
            self.bus_pirate.pullup_voltage_select()
