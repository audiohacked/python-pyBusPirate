""" UART class """

from buspirate.base import BusPirate

class UART(BusPirate):
    """ UART BitBanging on the BusPirate """
    def enter(self):
        """
        Enter BitBang Mode on the BusPirate

        :return: returns Success or Failure
        """
        self.write(0x03)
        return self.read(4) == "ART1"


if __name__ == '__main__':
    pass
