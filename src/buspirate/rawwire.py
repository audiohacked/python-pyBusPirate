""" RawWire class """

from buspirate.base import BusPirate

class RawWire(BusPirate):
    """ RawWire BitBanging on the BusPirate """
    def enter(self):
        """
        Enter BitBang Mode on the BusPirate

        :returns: returns Success or Failure
        """
        self.write(0x05)
        return self.read(4) == "RAW1"


if __name__ == '__main__':
    pass
