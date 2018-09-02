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

""" OpenOCD JTAG class """

from buspirate.base import BusPirate

class JTAG(BusPirate):
    """ JTAG BitBanging on the BusPirate """
    @property
    def enter(self):
        """
        Enter JTAG Mode on the BusPirate

        :returns: returns Success or Failure
        """
        self.write(0x06)
        return self.read(4) == "1W01"


if __name__ == '__main__':
    pass
