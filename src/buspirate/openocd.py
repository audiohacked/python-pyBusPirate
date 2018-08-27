""" OpenOCD JTAG class """

from buspirate.base import BusPirate

class JTAG(BusPirate):
    """ JTAG BitBanging on the BusPirate """
    def enter(self):
        """
        Enter JTAG Mode on the BusPirate

        :returns: returns Success or Failure
        """
        self.write(0x06)
        return self.read(4) == "1W01"


if __name__ == '__main__':
    pass
