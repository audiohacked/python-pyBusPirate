"""
Unit Tests for BusPirate SPI class
"""
import unittest
from unittest import mock

from buspirate import uart


# pylint: disable=C0111,E1101
class BusPirateUartTest(unittest.TestCase):
    """ Unit Test class """
    @mock.patch('serial.Serial', autospec=True)
    def setUp(self, mock_serial): # pylint: disable=W0613,W0221
        """ Unit Test setup """
        self.bus_pirate = uart.UART("/dev/ttyUSB0")

    def tearDown(self):
        """ Unit Test cleanup """
        pass

    def test_enter(self):
        self.bus_pirate.serial.read.return_value = "ART1"
        self.assertEqual(self.bus_pirate.enter(), True)
        self.bus_pirate.serial.write.assert_called_with(0x03)

    def test_mode(self):
        self.bus_pirate.serial.read.return_value = "ART1"
        self.assertEqual(self.bus_pirate.mode(), "ART1")
        self.bus_pirate.serial.write.assert_called_with(0x01)

    def test_echo_rx(self):
        start = 0b0
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.echo_rx(start), True)
        self.bus_pirate.serial.write.assert_called_with(0x02)

    def test_manual_baudrate(self):
        self.bus_pirate.serial.read.return_value = [0x01, 0x01, 0x01]
        self.assertEqual(self.bus_pirate.manual_baudrate(0x0000), True)
        self.bus_pirate.serial.write.assert_called_with([0x07, 0x0000])

    def test_bridge_mode(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.bridge_mode(), True)
        self.bus_pirate.serial.write.assert_called_with(0x0F)

    def test_uart_bulk_write(self):
        data = [idx for idx in range(1, 17)]
        self.bus_pirate.serial.read.side_effect = [0x01, data]
        result = self.bus_pirate.bulk_write(16, data)
        self.assertEqual(result, data)
        self.bus_pirate.serial.write.assert_any_call(0x10|0x0F)
        self.bus_pirate.serial.write.assert_any_call(data)

    def test_uart_speed(self):
        self.bus_pirate.serial.read.return_value = 0x01
        self.assertEqual(self.bus_pirate.uart_speed(uart.UartSpeed.BAUD_115200), True)
        self.bus_pirate.serial.write.assert_called_with(0x60|0x0A)

    def test_uart_configuration(self):
        self.bus_pirate.serial.read.return_value = 0x01
        result = self.bus_pirate.uart_configuration(uart.UartConfiguration.PinOutput.HIZ, \
                                                uart.UartConfiguration.DataBitsAndParity.EIGHT_NONE,
                                                    uart.UartConfiguration.StopBits.ONE,
                                                    uart.UartConfiguration.RxPolarity.IDLE_1)
        self.assertEqual(result, True)
        self.bus_pirate.serial.write.assert_called_with(0x80|0x00)
