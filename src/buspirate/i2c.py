""" I2C class """

from buspirate.base import BusPirate

class I2C(BusPirate):
    """ I2C BitBanging on the BusPirate """
    def enter(self):
        """
        Enter I2C Mode on the BusPirate

        :return: returns Success or Failure
        """
        self.write(0x02)
        return self.read(4) == "I2C1"


if __name__ == '__main__':
    pass
