"""
Unit Tests for BusPirate base class
"""
import unittest
from unittest import mock
from buspirate.base import BusPirate


# pylint: disable=C0111
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

    def test_mode(self):
        self.bus_pirate.serial.read.return_value = "SPI1"
        self.assertEqual(self.bus_pirate.mode(), "SPI1")

    def test_reset(self):
        self.assertEqual(self.bus_pirate.reset(), None)

    def test_configure_pins(self):
        self.assertEqual(self.bus_pirate.configure_pins(), None)

    def test_set_pins(self):
        self.assertEqual(self.bus_pirate.set_pins(), None)

    def test_configure_peripherials(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.configure_peripherials(), True)

    def test_bulk_write(self):
        self.bus_pirate.serial.read.side_effect = [0x01, bytearray([idx for idx in range(1, 17)])]
        data = [idx for idx in range(1, 17)]
        result = self.bus_pirate.bulk_write(16, data)
        self.assertEqual(result, bytearray(data))

    def test_bulk_write_fail(self):
        self.bus_pirate.serial.read.side_effect = [0x00, bytearray([idx for idx in range(1, 17)])]
        data = [idx for idx in range(1, 17)]
        result = self.bus_pirate.bulk_write(16, data)
        self.assertEqual(result, bytearray())

    def test_bulk_write_data_is_none(self):
        self.bus_pirate.serial.read.side_effect = [0x01, bytearray([idx for idx in range(1, 17)])]
        data = [idx for idx in range(1, 17)]
        result = self.bus_pirate.bulk_write(16, None)
        self.assertEqual(result, bytearray(data))

    def test__write_then_read(self):
        data = [idx for idx in range(1, 17)]
        self.bus_pirate.serial.read.return_value = [0x01] + data
        result = self.bus_pirate._write_then_read(command=0x04, write_count=16,
                                                  read_count=len(data), write_data=data)
        self.assertEqual(result, bytearray(data))

    def test__write_then_read_fail(self):
        data = [idx for idx in range(1, 17)]
        self.bus_pirate.serial.read.return_value = [0x00] + data
        result = self.bus_pirate._write_then_read(command=0x04, write_count=16,
                                                  read_count=len(data), write_data=data)
        self.assertEqual(result, bytearray())
