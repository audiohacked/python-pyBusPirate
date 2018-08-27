""" BusPirate Base class """

from enum import IntEnum

import serial


class PinConfiguration(IntEnum):
    """ Enum for Peripherial Configuration """
    DISABLE = 0b0
    ENABLE = 0b1


class BusPirate(object):
    """ Base Class for BitBanging on BusPirate """
    def __init__(self, port: str,
                 baudrate: int = 115200,
                 # bytesize: int = serial.EIGHTBITS,
                 # parity: int = serial.PARITY_NONE,
                 # stopbits: int = serial.STOPBITS_ONE,
                 timeout: float = 0.10,
                 # xonxoff: bool = False,
                 # rtscts: bool = False,
                 # dsrdtr: bool = False,
                 write_timeout: float = 0.10) -> None:
        """
        Init function that also executes the enter function

        :param port: The serial port
        :type port: str.
        :param baudrate: The serial bitrate
        :type baudrate: int.
        :param bytesize: The serial byte size
        :type bytesize: int.
        :param parity: The serial parity
        :type parity: int.
        :param stopbits: The serial stop bits
        :type stopbits: int.
        :param timeout: The serial read timeout (default is 0.10 seconds)
        :type timeout: float.
        :param xonxoff: The serial hardware control
        :type xonxoff: bool.
        :param rtscts: The serial hardware RTS/CTS
        :type rtscts: bool.
        :param dsrdtr: The serial hardware DSR/DTR
        :type dsrdtr: bool.
        :param write_timeout: The serial write timeout (default is 0.10 seconds)
        :type write_timeout: float.

        :returns: returns nothing
        """
        self.pass_to_super = locals()
        # self.pass_to_super.pop('self')
        # self.pass_to_super.pop('serial_class')
        # self.pass_to_super.pop('__class__')
        # super(BusPirate, self).__init__(**self.pass_to_super)
        self.serial = serial.Serial(**self.pass_to_super)
        self.serial.open()
        self.enter()

    def write(self, data: bytes = None) -> None:
        """
        Send Data to BusPirate

        :param data: The data to send over serial
        :type data: bytes

        :returns: returns nothing
        """
        self.serial.write(data)

    def read(self, count: int = 1) -> bytes:
        """
        Receive Data from BusPirate

        :param count: The number of bytes to receive over serial
        :type count: int.

        :returns: returns bytes of data
        :rtype: bytes
        """
        return self.serial.read(count)

    def enter(self) -> bool:
        """
        Enter BitBang Mode on the BusPirate

        :returns: returns Success or Failure
        :rtype: bool.
        """
        for _ in range(20):
            self.write(0x00)
            return self.read(5) == "BBIO1"

    def mode(self) -> str:
        """
        Get Version and Mode

        :returns: returns Success or Failure
        :rtype: bool
        """
        self.write(0x01)
        return self.read(4)

    def reset(self):
        """
        Reset BitBang Mode

        :returns: returns nothing
        """
        self.write(0x0F)

    def configure_pins(self):
        """
        Configure BusPirate Pins
        """
        pass

    def set_pins(self):
        """
        Set BusPirate Pins
        """
        pass

    def configure_peripherials(self,
                               power: int = PinConfiguration.DISABLE,
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

        :returns: returns Success or Failure
        :rtype: bool.
        """
        data = 0
        data += int(power)<<3
        data += pull_ups<<2
        data += aux<<1
        data += chip_select
        self.write(0x40|data)
        return self.read(1) == 0x01

    def bulk_write(self, count: int = 16, data: bytes = None) -> bytes:
        """
        Send Bulk Data for Write
        """
        self.write(0x10|count-1)
        if self.read(1) == 0x01:
            if data is None:
                data = bytes(count)
            self.write(data)
            return self.read(count)
        return bytes()

    def _write_then_read(self,
                         command: int = 0,
                         write_count: int = 0,
                         read_count: int = 0,
                         write_data: bytes = None) -> bytes:
        """
        Write then Read; used by SPI, I2C, etc

        :param command: The command byte for write_then_read
        :type command: int.
        :param write_count: The number of bytes to write
        :type write_count: int.
        :param read_count: The number of bytes to read
        :type read_count: int.
        :param write_data: The data bytes to write
        :type write_data: bytes.

        :returns: returns data read from Bus
        :rtype: bytes
        """
        assert len(write_data) == write_count, "Given data has incorrect length!"
        send_buffer: bytes = [command, write_count, read_count, write_data]
        self.write(send_buffer)
        recv_buffer = self.read(read_count+1)
        if recv_buffer[0] is 0x01:
            if len(recv_buffer[1:]) is read_count:
                return recv_buffer[1:]
        return bytes()


if __name__ == '__main__':
    pass
