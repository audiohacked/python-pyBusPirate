#!/usr/bin/env python
# encoding: utf-8
"""
Created by Sean Nelson on 2009-09-20.
Copyright 2009 Sean Nelson <audiohacked@gmail.com>

This file is part of pyBusPirate.

pyBusPirate is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyBusPirate is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyBusPirate.  If not, see <http://www.gnu.org/licenses/>.
"""

from SPIFlash import SPIFlash
from pyBusPirate.crc16 import *

write = 0
if __name__ == '__main__':
	if write is 0:
		spi_flash = SPIFlash()
		o = open("output.bin", 'wb+')
		spi_flash.flash_read(size=256*1024)
	else:
		spi_flash = SPIFlash()
		i = open("firmware.bin", 'rb')
		spi_flash.from_file(ipf=i)
		spi_flash.in_data[0x36:0x3B] = array('B', [0x0, 0x19, 0xFD, 0xA0, 0x96, 0xF6])
		crc = crc16(spi_flash.in_data[0x2C:])
		spi_flash.in_data[0x2A] = (crc>>8)
		spi_flash.in_data[0x2B] = (crc&0xFF)
		spi_flash.flash_write(size=0x200, data=spi_flash.in_data)

