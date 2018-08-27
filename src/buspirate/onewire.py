""" 1Wire Base class """

from buspirate.base import BusPirate

class OneWire(BusPirate):
    """ OneWire BitBanging on the BusPirate """
    def enter(self):
        """
        Enter OneWire Mode on the BusPirate

        :returns: returns Success or Failure
        """
        self.write(0x04)
        return self.read(4) == "1W01"


if __name__ == '__main__':
    pass
