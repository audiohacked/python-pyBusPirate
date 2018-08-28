""" pyBusPirate Utilities """

from buspirate.base import BusPirate

class Voltage(BusPirate):
    """ Voltage BitBang """
    def take_once(self):
        """
        Voltage Take Once

        :returns: returns Success or Failure
        :rtype: bool.
        """
        self.write(0x14)
        return self.read(1) == 0x01

    def continuous(self):
        """
        Voltage Continuous

        :returns: returns Success or Failure
        :rtype: bool.
        """
        self.write(0x15)
        return self.read(1) == 0x01


class SelfTests(BusPirate):
    """ Self-Tests on BusPirate """
    def short_test(self):
        """
        Short Self-Tests

        :returns: returns nothing
        """
        self.write(0x10)

    def long_test(self):
        """
        Short Self-Tests

        :returns: returns nothing
        """
        self.write(0x11)

    def exit(self):
        """
        Exit from Self-Tests

        :returns: returns Success or Failure
        :rtype: bool.
        """
        self.write(0xff)
        return self.read(1) == 0x01


class PWM(BusPirate):
    """ PWM BitBang """
    def setup(self):
        """
        PWM Setup

        :returns: returns Success or Failure
        :rtype: bool.
        """
        self.write(0x12)
        return self.read(1) == 0x01

    def clear(self):
        """
        PWM Clear

        :returns: returns Success or Failure
        :rtype: bool.
        """
        self.write(0x13)
        return self.read(1) == 0x01

    def disable(self):
        """
        PWM Disable

        :returns: returns Success or Failure
        :rtype: bool.
        """
        self.write(0x13)
        return self.read(1) == 0x01


class Frequency(BusPirate):
    """ Frequency Measurements on BusPirate """
    def measure(self):
        """
        Frequency Disable

        :returns: returns Success or Failure
        :rtype: bool.
        """
        self.write(0x16)
        return self.read(1) == 0x01


if __name__ == '__main__':
    pass
