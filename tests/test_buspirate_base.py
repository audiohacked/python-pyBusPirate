"""
Unit Tests for BusPirate class
"""
import pprint
import unittest
import unittest.mock as mock
from buspirate.base import BusPirate

class BusPirateTest(unittest.TestCase):
    @mock.patch('serial.Serial', autospec=True)
    def setUp(self, mock_serial):
        self.bp = BusPirate("/dev/ttyUSB0", serial_class=mock_serial)

    def tearDown(self):
        pass

    def test_enter(self):
        self.bp.serial.read.return_value = "BBIO1"
        self.assertTrue(self.bp.enter())
        
    def test_mode(self):
        self.bp.serial.read.return_value = "SPI1"
        self.assertEqual(self.bp.mode(), "SPI1")
    
    def test_reset(self):
        self.assertFalse(self.bp.reset())

    def test_configure_pins(self):
        self.assertFalse(self.bp.configure_pins())

    def test_set_pins(self):
        self.assertFalse(self.bp.set_pins())

    def test_configure_peripherials(self):
        self.bp.serial.read.return_value = 0x01
        self.assertTrue(self.bp.configure_peripherials())
    
    def test_bulk_write(self):
        self.bp.serial.read.side_effect = [0x01, bytearray([idx for idx in range(1,17)])]
        data = [idx for idx in range(1,17)]
        result = self.bp.bulk_write(16, data)
        self.assertEqual(result, bytearray(data))
        
    def test_bulk_write_fail(self):
        self.bp.serial.read.side_effect = [0x00, bytearray([idx for idx in range(1,17)])]
        data = [idx for idx in range(1,17)]
        result = self.bp.bulk_write(16, data)
        self.assertEqual(result, bytearray())
        
    def test_bulk_write_data_is_none(self):
        self.bp.serial.read.side_effect = [0x01, bytearray([idx for idx in range(1,17)])]
        data = [idx for idx in range(1,17)]
        result = self.bp.bulk_write(16, None)
        self.assertEqual(result, bytearray(data))
        
    def test__write_then_read(self):
        data = [idx for idx in range(1, 17)]
        self.bp.serial.read.return_value = [0x01] + data
        result = self.bp._write_then_read(command=0x04, write_count=16, read_count=len(data),
                                          write_data=data)
        self.assertEqual(result, bytearray(data))

    def test__write_then_read_fail(self):
        data = [idx for idx in range(1, 17)]
        self.bp.serial.read.return_value = [0x00] + data
        result = self.bp._write_then_read(command=0x04, write_count=16, read_count=len(data),
                                          write_data=data)
        self.assertEqual(result, bytearray())
