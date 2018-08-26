"""
Unit Tests for BusPirate SPI class
"""
import unittest
from unittest import mock
from buspirate import i2c


# pylint: disable=C0111
class BusPirateI2CTest(unittest.TestCase):
    @mock.patch('serial.Serial', autospec=True)
    def setUp(self, mock_serial): # pylint: disable=W0613,W0221
        self.bus_pirate = i2c.I2C("/dev/ttyUSB0")

    def tearDown(self):
        pass

    def test_exit(self):
        self.bus_pirate.serial.read.return_value = "BBIO1"
        self.assertEqual(self.bus_pirate.exit(), True)

    def test_mode(self):
        self.bus_pirate.serial.read.return_value = "I2C1"
        self.assertEqual(self.bus_pirate.mode(), True)

    def test_enter(self):
        self.bus_pirate.serial.read.return_value = "I2C1"
        self.assertEqual(self.bus_pirate.enter(), True)

    def test_start_bit(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.start_bit(), True)

    def test_stop_bit(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.stop_bit(), True)

    def test_read_byte(self) -> bytes:
        self.bus_pirate.serial.read.side_effect = [0x01, 0xFF]
        self.assertEqual(self.bus_pirate.read_byte(), True)

    def test_ack_bit(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.ack_bit(), True)

    def test_nack_bit(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.nack_bit(), True)

    def test_sniff(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.sniff(), None)

    def test_pullup_voltage_select(self):
        self.assertEqual(self.bus_pirate.pullup_voltage_select(), None)

    def test_i2c_speed(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.i2c_speed(i2c.I2CSpeed.SPEED_50KHZ), True)

    def test_write_then_read(self):
        data_len = 128
        data = [idx for idx in range(1, data_len+1)]
        self.bus_pirate.serial.read.return_value = [0x01] + data
        result = self.bus_pirate.write_then_read(data_len, data_len, data)
        self.assertEqual(result, bytearray(data))

    def test_extend_aux(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.extend_aux(i2c.I2CExtendAux.LOW), True)
