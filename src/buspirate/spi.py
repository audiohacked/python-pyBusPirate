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

""" SPI class """

from enum import IntEnum

from buspirate.base import BusPirate


class CsLevel(IntEnum):
    """ Enum for Chip Select Level """
    LOW = 0b0
    HIGH = 0b1


class CsSniffTrigger(IntEnum):
    """ Enum for Chip Select Sniffer Trigger """
    LOW = 0b10
    ALL = 0b01


class SpiSpeed(IntEnum):
    """ Enum for SPI Speeds """
    SPEED_30KHZ = 0b000
    SPEED_125KHZ = 0b001
    SPEED_250KHZ = 0b010
    SPEED_1MHZ = 0b011
    SPEED_2MHZ = 0b100
    SPEED_2P6MHZ = 0b101
    SPEED_4MHZ = 0b110
    SPEED_8MHZ = 0b111


class SpiConfiguration(object):
    """ SPI Configuration Enum Base """
    # def __getattr__(self, key):
    #     """
    #     Return an attribute of the class (fallback)
    #
    #     :returns: returns contents of class
    #     :rtype: str.
    #     """
    #     pass
    #
    # def __getattribute__(self, key):
    #     """
    #     Return an attribute of the class
    #
    #     :returns: returns contents of class
    #     :rtype: str.
    #     """
    #     pass
    #
    # def __str__(self) -> str:
    #     """
    #     Return string of the class
    #
    #     :returns: returns contents of class
    #     :rtype: str.
    #     """
    #     return str(self.__dict__)
    #
    # def __eq__(self, other: object = None) -> bool:
    #     """
    #     Compare SPI Configurations
    #
    #     :returns: returns a boolean
    #     :rtype: bool.
    #     """
    #     return self == other

    class PinOutput(IntEnum):
        """ Enum for Pin Output """
        HIZ = 0b0
        PIN_HIZ = 0b0
        V3P3 = 0b1
        PIN_3P3V = 0b1

    class ClockPhase(IntEnum):
        """ Enum for Clock Phase """
        LOW = 0b0

    class ClockEdge(IntEnum):
        """ Enum for Clock Edge """
        IDLE_TO_ACTIVE = 0b0
        ACTIVE_TO_IDLE = 0b1

    class SampleTime(IntEnum):
        """ Enum for Sample Time """
        MIDDLE = 0b0


class SPI(BusPirate):
    """ SPI BitBanging on the BusPirate """
    @property
    def enter(self) -> bool:
        """
        Enter BitBang Mode on the BusPirate

        :returns: returns Success or Failure
        :rtype: bool.
        """
        self.write(0x01)
        return self.read(4) == "SPI1"

    @property
    def cs(self):
        """ Chip Select Property Getter """
        return self._cs

    @cs.setter
    def cs(self, value):
        """ Chip Select Property Setter """
        self._cs = value
        self.chip_select(value)

    def chip_select(self, level: int = CsLevel.LOW) -> bool:
        """
        SPI Chip Select

        :param level: The Active Level for SPI Chip Select
        :type level: int.

        :returns: returns Success or Failure
        :rtype: bool.
        """
        self.write(0x02|level)
        return self.read(1) is 0x01

    def sniff(self, trigger: int = CsSniffTrigger.LOW) -> bool:
        """
        SPI Sniffer

        :param trigger: The trigger type for SPI Sniffer
        :type trigger: int.

        :returns: returns Success or Failure
        :rtype: bool.
        """
        self.write(0x0C|trigger)
        return self.read(1) == 0x01

    @property
    def speed(self):
        """ Speed Property Getter """
        return self._speed

    @speed.setter
    def speed(self, value):
        """ Speed Property Setter """
        self._speed = value
        return self.spi_speed(value)

    def spi_speed(self, spi_speed: int = SpiSpeed.SPEED_30KHZ) -> bool:
        """
        SPI Speed Configuration

        :param spi_speed: The SPI Clock Rate
        :type spi_speed: int.

        :returns: returns Success or Failure
        :rtype: bool
        """
        self.write(0x60|spi_speed)
        return self.read(1) == 0x01

    @property
    def config(self):
        """ Pin Config Property Getter """
        return self._config

    @config.setter
    def config(self, value):
        """ Ping Config Property Setter """
        self._config = value
        pin_outputs = value & 0b1000
        clock_phase = value & 0b0100
        clock_edges = value & 0b0010
        sampletimes = value & 0b0001
        return self.spi_configuration(pin_outputs, clock_phase, clock_edges, sampletimes)

    def spi_configuration(self,
                          pin_output: int = SpiConfiguration.PinOutput.HIZ,
                          clock_phase: int = SpiConfiguration.ClockPhase.LOW,
                          clock_edge: int = SpiConfiguration.ClockEdge.IDLE_TO_ACTIVE,
                          sample_time: int = SpiConfiguration.SampleTime.MIDDLE) -> bool:
        """
        SPI Configuration

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
        spi_configuration = 0
        spi_configuration += pin_output<<3
        spi_configuration += clock_phase<<2
        spi_configuration += clock_edge<<1
        spi_configuration += sample_time
        self.write(0x80|spi_configuration)
        return self.read(1) == 0x01

    def write_then_read(self,
                        write_count: int = 0,
                        read_count: int = 0,
                        write_data: bytes = None) -> bytes:
        """
        SPI Write then Read

        :param write_count: The number of bytes to write
        :type write_count: int.
        :param read_count: The number of bytes to read
        :type read_count: int.
        :param write_data: The data bytes to write
        :type write_data: bytes.

        :returns: returns data read from SPI
        :rtype: bytes
        """
        return super()._write_then_read(0x04, write_count, read_count, write_data)

    def write_then_read_with_no_cs(self,
                                   write_count: int = 0,
                                   read_count: int = 0,
                                   write_data: bytes = None) -> bool:
        """
        SPI Write then Read with No Chip Select transistion

        :param write_count: The number of bytes to write
        :type write_count: int.
        :param read_count: The number of bytes to read
        :type read_count: int.
        :param write_data: The data bytes to write
        :type write_data: bytes.

        :returns: returns data read from SPI
        :rtype: bytes
        """
        return super()._write_then_read(0x05, write_count, read_count, write_data)


if __name__ == '__main__':
    pass
