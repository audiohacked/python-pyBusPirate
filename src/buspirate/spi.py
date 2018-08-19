""" SPI class """

from enum import Enum
from buspirate.base import BusPirate


class CsLevel(Enum):
    """ Enum for Chip Select Level """
    LOW = 0b0
    HIGH = 0b1


class CsSniffTrigger(Enum):
    """ Enum for Chip Select Sniffer Trigger """
    LOW = 0b10
    ALL = 0b01


class PinConfiguration(Enum):
    """ Enum for Peripherial Configuration """
    DISABLE = 0b0
    ENABLE = 0b1


class SpiSpeed(Enum):
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
    def __str__(self) -> str:
        """
        Return string of the class

        :return: returns contents of class
        :rtype: str.
        """
        return str(self.__dict__)

    def __eq__(self, other: object = None) -> bool:
        """
        Compare SPI Configurations

        :return: returns a boolean
        :rtype: bool.
        """
        return self == other

    class PinOutput(Enum):
        """ Enum for Pin Output """
        HIZ = 0b0
        PIN_HIZ = 0b0
        V3P3 = 0b1
        PIN_3P3V = 0b1

    class ClockPhase(Enum):
        """ Enum for Clock Phase """
        LOW = 0b0

    class ClockEdge(Enum):
        """ Enum for Clock Edge """
        IDLE_TO_ACTIVE = 0b0
        ACTIVE_TO_IDLE = 0b1

    class SampleTime(Enum):
        """ Enum for Sample Time """
        MIDDLE = 0b0


class SPI(BusPirate):
    """ SPI BitBanging on the BusPirate """
    def enter(self) -> bool:
        """
        Enter BitBang Mode on the BusPirate

        :return: returns Success or Failure
        :rtype: bool.
        """
        self.write(0x01)
        return self.read(4) == "SPI1"

    def chip_select(self, level: int = CsLevel.LOW) -> bool:
        """
        SPI Chip Select

        :param level: The Active Level for SPI Chip Select
        :type level: int.

        :return: returns Success or Failure
        :rtype: bool.
        """
        self.write(0x02|level)
        return self.read(1) is 0x01

    def sniff(self, trigger: int = CsSniffTrigger.LOW) -> bool:
        """
        SPI Sniffer

        :param trigger: The trigger type for SPI Sniffer
        :type trigger: int.

        :return: returns Success or Failure
        :rtype: bool.
        """
        self.write(0x0C|trigger)
        return self.read(1) == 0x01

    def bulk_transfer_start(self, transfer: int = 16) -> bool:
        """
        SPI Transfer

        :param transfer: The number of bytes to bulk transfer (1 to 16 bytes)
        :type transfer: int.

        :return: returns Success or Failure
        :rtype: bool.
        """
        self.write(0x10|(transfer-1))
        return self.read(1) == 0x01

    def configure_peripherials(self, power: int = PinConfiguration.DISABLE,
                               pull_ups: int = PinConfiguration.DISABLE,
                               aux: int = PinConfiguration.DISABLE,
                               chip_select: int = PinConfiguration.DISABLE) -> bool:
        """
        SPI Configure Peripherial Pins

        :param power: The Pin Configuration for Power Pins
        :type power: int.

        :param pull_ups: The Pin Configuration for Pull Up Pins
        :type pull_ups: int.

        :param aux: The Pin Configuration for AUX pin
        :type aux: int.

        :param chip_select: The Pin Configuration for Chip Select Pin
        :type chip_select: int.

        :return: returns Success or Failure
        :rtype: bool.
        """
        data = 0
        data += power<<3
        data += pull_ups<<2
        data += aux<<1
        data += chip_select
        self.write(0x40|data)
        return self.read(1) == 0x01

    def spi_speed(self, spi_speed: int = SpiSpeed.SPEED_30KHZ) -> bool:
        """
        SPI Speed Configuration

        :param spi_speed: The SPI Clock Rate
        :type spi_speed: int.

        :return: returns Success or Failure
        :rtype: bool
        """
        self.write(0x60|spi_speed)
        return self.read(1) == 0x01

    def spi_configuration(self, pin_output: int = SpiConfiguration.PinOutput.HIZ,
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

        :return: returns Success or Failure
        :rtype: bool.
        """
        spi_configuration = 0
        spi_configuration += pin_output<<3
        spi_configuration += clock_phase<<2
        spi_configuration += clock_edge<<1
        spi_configuration += sample_time
        self.write(0x80|spi_configuration)
        return self.read(1) == 0x01

    def write_then_read(self):
        """
        SPI Write then Read
        """
        pass

    def write_then_read_no_cs(self):
        """
        SPI Write then Read with No Chip Select transistion
        """
        pass


if __name__ == '__main__':
    pass
