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

""" RawWire class """

from enum import IntEnum

from buspirate.base import BusPirate


class RawWireSpeed(IntEnum):
    """ Enum for RawWire Speeds """
    SPEED_5KHZ = 0b000
    SPEED_50KHZ = 0b001
    SPEED_100KHZ = 0b010
    SPEED_400KHZ = 0b011


class RawWireConfiguration(object):
    """ RawWire Configuration Enum Base """
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
        HIZ = 0b0000
        V3P3 = 0b1000
        PIN_HIZ = 0b0000
        PIN_3P3V = 0b1000

    class WireProtocol(IntEnum):
        """ Enum for Wire Protocol """
        PROTOCOL_2WIRE = 0b0000
        PROTOCOL_3WIRE = 0b0100

    class BitOrder(IntEnum):
        """ Enum for Bit Order """
        MSB = 0b0000
        LSB = 0b0010

    class NotUsed(IntEnum):
        """ Enum for Position Z in RawWireConfiguration """
        pass


class RawWire(BusPirate):
    """ RawWire BitBanging on the BusPirate """
    @property
    def exit(self):
        """
        Exit RawWire Mode

        :returns: returns Success or Failure
        """
        self.write(0x00)
        return self.read(5) == "BBIO1"


    @property
    def enter(self):
        """
        Enter RawWire Mode

        :returns: returns Success or Failure
        """
        self.write(0x05)
        return self.read(4) == "RAW1"


    @property
    def start_bit(self):
        """
        Start Bit

        :returns: returns Success or Failure
        """
        self.write(0x02)
        return self.read(1) == 0x01


    @property
    def stop_bit(self):
        """
        Stop Bit

        :returns: returns Success or Failure
        """
        self.write(0x03)
        return self.read(1) == 0x01


    @property
    def cs_low(self):
        """
        Toggle Chip Select Low

        :returns: returns Success or Failure
        """
        self.write(0x04)
        return self.read(1) == 0x01


    @property
    def cs_high(self):
        """
        Toggle Chip Select High

        :returns: returns Success or Failure
        """
        self.write(0x05)
        return self.read(1) == 0x01


    def read_byte(self):
        """
        Read Byte from Bus

        :returns: returns Success or Failure
        """
        self.write(0x06)
        return self.read(1)


    def read_bit(self):
        """
        Read Bit From Bus

        :returns: returns Success or Failure
        """
        self.write(0x07)
        return self.read(1)


    def peek(self):
        """
        Peek at Bus without toggling CS or something

        :returns: returns Success or Failure
        """
        self.write(0x08)
        return self.read(1)


    def clock_tick(self):
        """
        Jiggle Clock

        :returns: returns Success or Failure
        """
        self.write(0x09)
        return self.read(1) == 0x01


    @property
    def clock_low(self):
        """
        Toggle Clock Low

        :returns: returns Success or Failure
        """
        self.write(0x0A)
        return self.read(1) == 0x01


    @property
    def clock_high(self):
        """
        Toggle Clock High

        :returns: returns Success or Failure
        """
        self.write(0x0B)
        return self.read(1) == 0x01


    @property
    def data_low(self):
        """
        Toggle Data line Low

        :returns: returns Success or Failure
        """
        self.write(0x0C)
        return self.read(1) == 0x01


    @property
    def data_high(self):
        """
        Toggle Data line High

        :returns: returns Success or Failure
        """
        self.write(0x0D)
        return self.read(1) == 0x01


    def bulk_clock_ticks(self, count: int = 16):
        """
        Send Bulk Clock ticks

        :returns: returns Success or Failure
        """
        if count == 0 or count > 16:
            raise ValueError
        self.write(0x20|count-1)
        return self.read(1) == 0x01


    def bulk_bits(self, count: int = 8, data_byte: int = 0x00):
        """
        Send Bulk bits of a byte

        :returns: returns Success or Failure
        """
        if count == 0 or count > 8:
            raise ValueError
        self.write(0x30|count-1)
        self.write(data_byte)
        return self.read(1) == 0x01


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
        self.rawwire_speed(value)

    def rawwire_speed(self, rawwire_speed: int = RawWireSpeed.SPEED_400KHZ) -> bool:
        """
        Raw Wire Speed Configuration

        :param rawwire_speed: The Clock Rate
        :type rawwire_speed: int.

        :returns: returns Success or Failure
        :rtype: bool
        """
        self.write(0x60|rawwire_speed)
        return self.read(1) == 0x01


    @property
    def config(self):
        """ Configuration Property Getter """
        return self._config

    @config.setter
    def config(self, value):
        """ Configuration Property Setter """
        self._config = value
        p_output = value & 0b1000
        protocol = value & 0b0100
        bitorder = value & 0b0010
        return self.rawwire_config(p_output, protocol, bitorder)

    def rawwire_config(self,
                       pin_output: int = RawWireConfiguration.PinOutput.HIZ,
                       wire_protocol: int = RawWireConfiguration.WireProtocol.PROTOCOL_2WIRE,
                       bit_order: int = RawWireConfiguration.BitOrder.MSB) -> bool:
        """
        Raw Wire Configuration

        :param pin_output: The Pin Configuration for Pin Output
        :type pin_output: int.

        :param wire_protocol: The Raw Wire Configuration for Protocol
        :type wire_protocol: int.

        :param bit_order: The Raw Wire Configuration for First Bit Order
        :type bit_order: int.

        :returns: returns Success or Failure
        :rtype: bool.
        """
        rawwire_configuration = 0
        rawwire_configuration += pin_output
        rawwire_configuration += wire_protocol
        rawwire_configuration += bit_order

        self.write(0x80|rawwire_configuration)
        return self.read(1) == 0x01


if __name__ == '__main__':
    pass
