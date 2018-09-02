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

""" I2C class """

from enum import IntEnum

from buspirate.base import BusPirate


class I2CSpeed(IntEnum):
    """ Enum for I2C Speeds """
    SPEED_5KHZ = 0b000
    SPEED_50KHZ = 0b001
    SPEED_100KHZ = 0b010
    SPEED_400KHZ = 0b011


class I2CExtendAux(IntEnum):
    """ Enum for I2C Extend Aux """
    LOW = 0x00
    HIGH = 0x01
    HIZ = 0x02
    AUX_READ = 0x03
    USE_AUX = 0x10
    USE_CS = 0x20


class I2C(BusPirate):
    """ I2C BitBanging on the BusPirate """
    @property
    def exit(self) -> bool:
        """
        Exit to BitBang mode

        :returns: returns Success or Failure
        :rtype: bool
        """
        self.write(0x00)
        return self.read(5) == "BBIO1"

    @property
    def mode(self) -> bool:
        """
        Get Version and Mode

        :returns: returns Success or Failure
        :rtype: bool
        """
        self.write(0x01)
        return self.read(4) == "I2C1"

    @property
    def enter(self) -> bool:
        """
        Enter I2C Mode on the BusPirate

        :returns: returns Success or Failure
        :rtype: bool
        """
        self.write(0x02)
        return self.read(4) == "I2C1"

    @property
    def start_bit(self) -> bool:
        """
        Send I2C Start bit

        :returns: returns Success or Failure
        :rtype: bool
        """
        self.write(0x02)
        return self.read(1) == 0x01

    @property
    def stop_bit(self) -> bool:
        """
        Send I2C Stop bit

        :returns: returns Success or Failure
        :rtype: bool
        """
        self.write(0x03)
        return self.read(1) == 0x01

    def read_byte(self) -> bytes:
        """
        Read I2C Byte

        :returns: returns Success or Failure
        :rtype: bool
        """
        self.write(0x04)
        return self.read(1) == 0x01

    @property
    def ack_bit(self) -> bool:
        """
        Send I2C ACK bit

        :returns: returns Success or Failure
        :rtype: bool
        """
        self.write(0x06)
        return self.read(1) == 0x01

    @property
    def nack_bit(self) -> bool:
        """
        Send I2C NACK bit

        :returns: returns Success or Failure
        :rtype: bool
        """
        self.write(0x07)
        return self.read(1) == 0x01

    def sniff(self) -> bool:
        """
        Sniff I2C Bus

        :returns: returns nothing
        """
        self.write(0x0F)

    def pullup_voltage_select(self) -> None:
        """
        Select Pull-Up Voltage

        Unimplmented!
        """
        raise NotImplementedError

    @property
    def speed(self):
        """ Speed Property Getter """
        return self._speed


    @speed.setter
    def speed(self, value):
        """ Speed Property Setter """
        self._speed = value
        return self.i2c_speed(value)

    def i2c_speed(self, i2c_speed: int = I2CSpeed.SPEED_5KHZ):
        """
        SPI Speed Configuration

        :param i2c_speed: The SPI Clock Rate
        :type i2c_speed: int.

        :returns: returns Success or Failure
        :rtype: bool.
        """
        self.write(0x60|i2c_speed)
        return self.read(1) == 0x01

    def write_then_read(self,
                        write_count: int = 0,
                        read_count: int = 0,
                        write_data: bytes = None) -> bytes:
        """
        I2C Write then Read

        :param write_count: The number of bytes to write
        :type write_count: int.
        :param read_count: The number of bytes to read
        :type read_count: int.
        :param write_data: The data bytes to write
        :type write_data: bytes.

        :returns: returns data read from SPI
        :rtype: bytes
        """
        return super()._write_then_read(0x08, write_count, read_count, write_data)

    def extend_aux(self, command: int = I2CExtendAux.LOW) -> bool:
        """
        I2C Extend Aux

        :param command: The Aux Config Command to send
        :type command: int

        :returns: returns Success or Failure
        :rtype: bool.
        """
        send_buffer: bytes = [0x09, command]
        self.write(send_buffer)
        return self.read(1) == 0x01

if __name__ == '__main__':
    pass
