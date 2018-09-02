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

""" 1Wire Base class """

from buspirate.base import BusPirate

class OneWire(BusPirate):
    """ OneWire BitBanging on the BusPirate """
    def exit(self):
        """
        Exit OneWire Mode on the BusPirate

        :returns: returns Success or Failure
        """
        self.serial.write(0x00)
        return self.read(5) == "BBIO1"

    def enter(self):
        """
        Enter OneWire Mode on the BusPirate

        :returns: returns Success or Failure
        """
        self.serial.write(0x04)
        return self.read(4) == "1W01"

    def read_byte(self):
        """
        Read 1 Byte from Interface

        :returns: returns Success or Failure
        """
        self.serial.write(0x04)
        return self.read(1)

    def rom_search(self):
        """
        Search for ROMs, successive reads are device address, terminates with 8 0xff

        :returns: returns Success or Failure
        """
        self.serial.write(0x08)
        return self.read(1) == 0x01

    def alarm_search(self):
        """
        Search for Alarms, successive reads are device address, terminates with 8 0xff

        :returns: returns Success or Failure
        """
        self.serial.write(0x09)
        return self.read(1) == 0x01

    def pullup_voltage_select(self) -> None:
        """
        Select Pull-Up Voltage

        Unimplmented!
        """
        raise NotImplementedError

if __name__ == '__main__':
    pass
