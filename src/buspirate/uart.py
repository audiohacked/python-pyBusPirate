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

""" UART class """

from enum import IntEnum
from buspirate.base import BusPirate


class UartSpeed(IntEnum):
    """ UART Speed Enum """
    BAUD_300 = 0b0000
    BAUD_1200 = 0b0001
    BAUD_2400 = 0b0010
    BAUD_4800 = 0b0011
    BAUD_9600 = 0b0100
    BAUD_19200 = 0b0101
    BAUD_31250 = 0b0110
    BAUD_MIDI = 0b0110
    MIDI = 0b0110
    BAUD_38400 = 0b0111
    BAUD_57600 = 0b1000
    BAUD_115200 = 0b1010


class UartConfiguration(object):
    """ UART Configuration Enum Base """
    class PinOutput(IntEnum):
        """ Enum for Pin Output """
        HIZ = 0b0
        PIN_HIZ = 0b0
        V3P3 = 0b1
        PIN_3P3V = 0b1

    class DataBitsAndParity(IntEnum):
        """ Enum for Data bits and Parity """
        EIGHT_NONE = 0b00
        EIGHT_EVEN = 0b01
        EIGHT_ODD = 0b10
        NINE_NONE = 0b11

    class StopBits(IntEnum):
        """ Enum for Stop bits """
        ONE = 0b0
        TWO = 0b1

    class RxPolarity(IntEnum):
        """ Enum for Rx Polarity """
        IDLE_1 = 0b0
        IDLE_0 = 0b1


class UART(BusPirate):
    """ UART BitBanging on the BusPirate """
    def enter(self) -> bool:
        """
        Enter UART Mode on the BusPirate

        :returns: returns Success or Failure
        """
        self.write(0x03)
        return self.read(4) == "ART1"

    def echo_rx(self, start_stop: int = 0) -> bool:
        """
        Enable disable RX Echoing

        :param start_stop: Give 0 for Start Echo, Give 1 to Stop Echo
        :type start_stop: int

        :returns: Success or Failure
        :rtype: bool
        """
        self.write(0x02|start_stop)
        return self.read(1) == 0x01

    def manual_baudrate(self, brg_register: int = 0x0000) -> bool:
        """
        Set Baudrate Manually

        :param brg_register: BRG Register value based on 32mhz osc, divider = 2, and BRGH = 1
        :type brg_register: int

        :returns: Success or Failure
        :rtype: bool
        """
        data = [0x07, brg_register]
        self.write(data)
        return self.read(3) == [0x01, 0x01, 0x01]

    def bridge_mode(self) -> bool:
        """
        Enable Bridge mode. Hard Reset BP to exit.

        :returns: Success or Failure
        :rtype: bool
        """
        self.write(0x0F)
        return self.read(1) == 0x01

    def uart_speed(self, baudrate: int = UartSpeed.BAUD_115200) -> bool:
        """
        Set UART Speed

        :param baudrate: Uart Baud Rates
        :type baudrate: int

        :returns: Success or Failure
        :rtype: bool
        """
        self.write(0x60|baudrate)
        return self.read(1) == 0x01

    def uart_configuration(self,
                           pin_output: int = UartConfiguration.PinOutput.HIZ,
                           databits_parity: int = UartConfiguration.DataBitsAndParity.EIGHT_NONE,
                           stop_bits: int = UartConfiguration.StopBits.ONE,
                           rx_polarity: int = UartConfiguration.RxPolarity.IDLE_1) -> bool:
        """
        UART Configuration

        :param pin_output: The Pin Configuration for Power Pins
        :type pin_output: int.

        :param clock_phase: The Pin Configuration for Pull Up Pins
        :type clock_phase: int.

        :param clock_edge: The Pin Configuration for AUX pin
        :type clock_edge: int.

        :param sample_time: The Pin Configuration for Chip Select Pin
        :type sample_time: int.

        :returns: returns Success or Failure
        :rtype: bool.
        """
        uart_configuration = 0
        uart_configuration += pin_output<<4
        uart_configuration += databits_parity<<2
        uart_configuration += stop_bits<<1
        uart_configuration += rx_polarity
        self.write(0x80|uart_configuration)
        return self.read(1) == 0x01

if __name__ == '__main__':
    pass
