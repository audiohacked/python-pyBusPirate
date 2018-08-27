"""
Unit Tests for BusPirate SPI class
"""
import unittest
from unittest import mock

from buspirate import spi


# pylint: disable=C0111
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
        self.assertEqual(self.bus_pirate.enter(), True)

    def test_chip_select_low(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.chip_select(spi.CsLevel.LOW), True)

    def test_sniff(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.sniff(spi.CsSniffTrigger.LOW), True)

    def test_spi_speed(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.spi_speed(spi.SpiSpeed.SPEED_8MHZ), True)

    def test_spi_configuration(self):
        self.bus_pirate.serial.read.return_value = 0x01
        result = self.bus_pirate.spi_configuration(spi.SpiConfiguration.PinOutput.HIZ,
                                                   spi.SpiConfiguration.ClockPhase.LOW,
                                                   spi.SpiConfiguration.ClockEdge.IDLE_TO_ACTIVE,
                                                   spi.SpiConfiguration.SampleTime.MIDDLE)
        self.assertEqual(result, True)

    def test_write_then_read(self):
        data_len = 128
        data = [idx for idx in range(1, data_len+1)]
        self.bus_pirate.serial.read.return_value = [0x01] + data
        result = self.bus_pirate.write_then_read(data_len, data_len, data)
        self.assertEqual(result, data)

    def test_write_then_read_with_no_cs(self):
        data_len = 128
        data = [idx for idx in range(1, data_len+1)]
        self.bus_pirate.serial.read.return_value = [0x01] + data
        result = self.bus_pirate.write_then_read_with_no_cs(data_len, data_len, data)
        self.assertEqual(result, data)
