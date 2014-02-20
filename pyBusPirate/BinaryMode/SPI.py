#!/usr/bin/env python
# encoding: utf-8
"""
Created by Sean Nelson on 2009-10-14.
Copyright 2009-2013 Sean Nelson <audiohacked@gmail.com>

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

from BitBang import *

class SPISpeed:
	_30KHZ = 0b000
	_125KHZ = 0b001
	_250KHZ = 0b010
	_1MHZ = 0b011
	_2MHZ = 0b100
	_2_6MHZ = 0b101
	_4MHZ = 0b110
	_8MHZ = 0b111

class SPICfg:
	OUT_TYPE = 0x8
	IDLE = 0x4
	CLK_EDGE = 0x2
	SAMPLE = 0x1

class SPI_OUT_TYPE:
	HIZ = 0
	_3V3 = 1
"""
	3.1 00000000 - Enter raw bitbang mode, reset to raw bitbang mode
	3.2 00000001 - Enter raw SPI mode, display version string
	3.3 0000001x - CS high (1) or low (0)
	3.4 000011XX - Sniff SPI traffic when CS low(10)/all(01)
	3.5 0001xxxx - Bulk SPI transfer, send/read 1-16 bytes (0=1byte!)
	3.6 0100wxyz - Configure peripherals w=power, x=pull-ups, y=AUX, z=CS
	3.7 01100xxx - SPI speed
	3.8 1000wxyz - SPI config, w=HiZ/3.3v, x=CKP idle, y=CKE edge, z=SMP sample
	3.9 00000100 - Write then read
		3.9.1 00000101 - Write then read, no CS
	3.10 AVR Extended Commands
"""
class SPI(BBIO):
	bulk_read = None
	def __init__(self, port='/dev/ttyUSB0', speed=115200, timeout=1):
		super(SPI, self).__init__(port, speed, timeout)

	def configure(self):
		if not super(SPI, self).configure():
			return False
		
		if not self.enter_SPI():
			return False

		return True

	def CS_Low(self):
		self.port.write(b"\x02")
		self.timeout(0.1)
		return self.response(1, True)

	def CS_High(self):
		self.port.write(b"\x03")
		self.timeout(0.1)
		return self.response(1, True)

	def low_nibble(self, nibble):
		self.port.write(chr(0x20 | nibble))
		self.timeout(0.1)
		return self.response(1, True)

	def high_nibble(self, nibble):
		self.port.write(chr(0x30 | nibble))
		self.timeout(0.1)
		return self.response(1, True)

	def cfg_spi(self, spi_cfg):
		self.port.write(chr(0x80 | spi_cfg))
		self.timeout(0.1)
		return self.response()

	def read_spi_cfg(self):
		self.port.write(b"\x90")
		self.timeout(0.1)
		return self.response(1, True)

