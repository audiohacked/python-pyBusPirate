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

from buspirate import rawwire


# pylint: disable=C0111,E1101
class BusPirateRawWireTest(unittest.TestCase):
    @mock.patch('serial.Serial', autospec=True)
    def setUp(self, mock_serial): # pylint: disable=W0613,W0221
        self.bus_pirate = rawwire.RawWire("/dev/ttyUSB0")

    def tearDown(self):
        pass

    def test_exit(self):
        self.bus_pirate.serial.read.return_value = "BBIO1"
        self.assertEqual(self.bus_pirate.exit, True)
        self.bus_pirate.serial.write.assert_called_with(0x00)

    def test_mode(self):
        self.bus_pirate.serial.read.return_value = "RAW1"
        self.assertEqual(self.bus_pirate.mode, "RAW1")
        self.bus_pirate.serial.write.assert_called_with(0x01)

    def test_enter(self):
        self.bus_pirate.serial.read.return_value = "RAW1"
        self.assertEqual(self.bus_pirate.enter, True)
        self.bus_pirate.serial.write.assert_called_with(0x05)

    def test_start_bit(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.start_bit, True)
        self.bus_pirate.serial.write.assert_called_with(0x02)

    def test_stop_bit(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.stop_bit, True)
        self.bus_pirate.serial.write.assert_called_with(0x03)

    def test_cs_low(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.cs_low, True)
        self.bus_pirate.serial.write.assert_called_with(0x04)

    def test_cs_high(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.cs_high, True)
        self.bus_pirate.serial.write.assert_called_with(0x05)

    def test_read_byte(self):
        self.bus_pirate.serial.read.side_effect = [0x01, 0xFF]
        self.assertEqual(self.bus_pirate.read_byte(), True)
        self.bus_pirate.serial.write.assert_called_with(0x06)

    def test_read_bit(self):
        self.bus_pirate.serial.read.side_effect = [0x01, 0x01]
        self.assertEqual(self.bus_pirate.read_bit(), True)
        self.bus_pirate.serial.write.assert_called_with(0x07)

    def test_peek(self):
        self.bus_pirate.serial.read.side_effect = [0x01, 0x01]
        self.assertEqual(self.bus_pirate.peek(), True)
        self.bus_pirate.serial.write.assert_called_with(0x08)

    def test_clock_tick(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.clock_tick(), True)
        self.bus_pirate.serial.write.assert_called_with(0x09)

    def test_clock_low(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.clock_low, True)
        self.bus_pirate.serial.write.assert_called_with(0x0A|0x00)

    def test_clock_high(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.clock_high, True)
        self.bus_pirate.serial.write.assert_called_with(0x0A|0x01)

    def test_data_low(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.data_low, True)
        self.bus_pirate.serial.write.assert_called_with(0x0C|0x00)

    def test_data_high(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.data_high, True)
        self.bus_pirate.serial.write.assert_called_with(0x0C|0x01)

    def test_rawwire_bulk_write(self):
        read_data = [0x00 for idx in range(1, 17)]
        write_data = [idx for idx in range(1, 17)]
        self.bus_pirate.serial.read.side_effect = [0x01, read_data]
        result = self.bus_pirate.bulk_write(16, write_data)
        self.assertEqual(result, read_data)
        self.bus_pirate.serial.write.assert_any_call(0x10|0x0F)
        self.bus_pirate.serial.write.assert_any_call(write_data)

    def test_bulk_clock_ticks(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.bulk_clock_ticks(16), True)
        self.bus_pirate.serial.write.assert_called_with(0x20|0x0F)

    def test_bulk_clock_ticks_zero(self):
        self.bus_pirate.serial.read.return_value = 0x01
        with self.assertRaises(ValueError):
            self.bus_pirate.bulk_clock_ticks(0)

    def test_bulk_bits(self):
        self.bus_pirate.serial.read.return_value = 0x01
        result = self.bus_pirate.bulk_bits(8, 0xFF)
        self.assertEqual(result, True)
        self.bus_pirate.serial.write.assert_any_call(0x30|0x07)
        self.bus_pirate.serial.write.assert_any_call(0xFF)

    def test_bulk_bits_zero_bits(self):
        self.bus_pirate.serial.read.return_value = 0x01
        with self.assertRaises(ValueError):
            self.bus_pirate.bulk_bits(0, 0xFF)

    def test_bulk_bits_nine_bits(self):
        self.bus_pirate.serial.read.return_value = 0x01
        with self.assertRaises(ValueError):
            self.bus_pirate.bulk_bits(9, 0xFF)

    @unittest.skip
    def test_bulk_bits_zero_bytes(self):
        self.bus_pirate.serial.read.return_value = 0x01
        with self.assertRaises(ValueError):
            self.bus_pirate.bulk_bits(8, 0x00)

    def test_pullup_voltage_select(self):
        with self.assertRaises(NotImplementedError):
            self.bus_pirate.pullup_voltage_select()

    def test_rawwire_speed(self):
        self.bus_pirate.speed = rawwire.RawWireSpeed.SPEED_100KHZ
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.speed, rawwire.RawWireSpeed.SPEED_100KHZ)
        self.bus_pirate.serial.write.assert_called_with(0x60|0x02)

    def test_rawwire_config(self):
        self.bus_pirate.config = 0b0000
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.config, 0b0000)
        self.bus_pirate.serial.write.assert_called_with(0x80|0x00)

    @unittest.skip
    def test_pic_write(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.pic_write(), True)
        self.bus_pirate.serial.write.assert_called_with(0x0C|0x01)

    @unittest.skip
    def test_pic_read(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.pic_read(), True)
        self.bus_pirate.serial.write.assert_called_with(0x0C|0x01)
