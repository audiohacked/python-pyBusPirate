""" BusPirate Base class """

import serial

class BusPirate(serial.Serial):
    """ Base Class for BitBanging on BusPirate """
    def __init__(self, port: str,
                 baudrate: int = 115200,
                 bytesize: int = serial.EIGHTBITS,
                 parity: int = serial.PARITY_NONE,
                 stopbits: int = serial.STOPBITS_ONE,
                 timeout: float = 0.10,
                 xonxoff: bool = False,
                 rtscts: bool = False,
                 dsrdtr: bool = False,
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

        :return: returns nothing
        """
        super().__init__(**locals())
        self.open()
        self.enter()

    def send(self, data: bytearray = None) -> None:
        """
        Send Data to BusPirate

        :param data: The data to send over serial
        :type data: bytearray

        :return: returns nothing
        """
        self.write(data)

    def recv(self, count: int = 1) -> bool:
        """
        Receive Data from BusPirate

        :param count: The number of bytes to receive over serial
        :type count: int.

        :return: returns bytes of data
        :rtype: bytearray
        """
        return self.read(count)

    def enter(self) -> bool:
        """
        Enter BitBang Mode on the BusPirate

        :return: returns Success or Failure
        :rtype: bool.
        """
        for _ in range(20):
            self.write(0x00)
            return self.read(5) == "BBIO1"

    def reset(self):
        """
        Reset BitBang Mode

        :return: returns nothing
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


if __name__ == '__main__':
    pass
