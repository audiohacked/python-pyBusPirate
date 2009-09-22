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

if __name__ == '__main__':
	o = open("output.bin", 'wb+')
	#i = open("input.bin", 'rb')
	spi_flash = SPIFlash(opf=o)
	spi_flash.flash_read(size=1024)
	#spi_flash.from_file(ipf=i)
	#spi_flash.flash_write()
