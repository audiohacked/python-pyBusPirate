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

from buspirate import spi


# pylint: disable=C0111,E1101
class BusPirateSpiTest(unittest.TestCase):
    """ Unit Test class """
    @mock.patch('serial.Serial', autospec=True)
    def setUp(self, mock_serial): # pylint: disable=W0613,W0221
        """ Unit Test setup """
        self.bus_pirate = spi.SPI("/dev/ttyUSB0")

    def tearDown(self):
        """ Unit Test cleanup """
        pass

    def test_enter(self):
        self.bus_pirate.serial.read.return_value = "SPI1"
        self.assertEqual(self.bus_pirate.enter, True)
        self.bus_pirate.serial.write.assert_called_with(0x01)

    def test_chip_select_high(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.chip_select(spi.CsLevel.HIGH), True)
        self.bus_pirate.serial.write.assert_called_with(0x02|0x01)

    def test_chip_select_low(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.chip_select(spi.CsLevel.LOW), True)
        self.bus_pirate.serial.write.assert_called_with(0x02|0x00)

    def test_sniff(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.sniff(spi.CsSniffTrigger.LOW), True)
        self.bus_pirate.serial.write.assert_called_with(0x0C|0x02)

    def test_spi_speed(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.spi_speed(spi.SpiSpeed.SPEED_8MHZ), True)
        self.bus_pirate.serial.write.assert_called_with(0x60|0x07)

    def test_spi_configuration(self):
        self.bus_pirate.serial.read.return_value = 0x01
        result = self.bus_pirate.spi_configuration(spi.SpiConfiguration.PinOutput.HIZ,
                                                   spi.SpiConfiguration.ClockPhase.LOW,
                                                   spi.SpiConfiguration.ClockEdge.IDLE_TO_ACTIVE,
                                                   spi.SpiConfiguration.SampleTime.MIDDLE)
        self.assertEqual(result, True)
        self.bus_pirate.serial.write.assert_called_with(0x80|0x00)

    def test_write_then_read(self):
        data_len = 128
        data = [idx for idx in range(1, data_len+1)]
        self.bus_pirate.serial.read.return_value = [0x01] + data
        result = self.bus_pirate.write_then_read(data_len, data_len, data)
        self.assertEqual(result, data)
        self.bus_pirate.serial.write.assert_called_with([0x04, 128, 128, data])

    def test_write_then_read_with_no_cs(self):
        data_len = 128
        data = [idx for idx in range(1, data_len+1)]
        self.bus_pirate.serial.read.return_value = [0x01] + data
        result = self.bus_pirate.write_then_read_with_no_cs(data_len, data_len, data)
        self.assertEqual(result, data)
        self.bus_pirate.serial.write.assert_called_with([0x05, 128, 128, data])
