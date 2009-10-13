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

import select
from .BBIO import BBIO

class SPISpeed:
	_30KHZ = 0b000
	_125KHZ = 0b001
	_250KHZ = 0b010
	_1MHZ = 0b011
	_2MHZ = 0b100
	_2_6MHZ = 0b101
	_4MHZ = 0b110
	_8MHZ = 0b111

class SPIPins:
	POWER = 0x8
	PULLUPS = 0x4
	AUX = 0x2
	CS = 0x1
	
class SPICfg:
	OUT_TYPE = 0x8
	IDLE = 0x4
	CLK_EDGE = 0x2
	SAMPLE = 0x1

class SPI_OUT_TYPE:
	HIZ = 0
	_3V3 = 1

class RawSPI(BBIO):
	bulk_read = None
	def __init__(self):
		BBIO.__init__(self)

	def CS_Low(self):
		self.port.write("\x02")
		select.select(None, None, None, 0.1)
		if self.port.read() is 0x01: return 1
		else: return 0

	def CS_High(self):
		self.port.write("\x03")
		select.select(None, None, None, 0.1)
		if self.port.read() is 0x01: return 1
		else: return 0

	def bulkTrans(self, byte_count=16, byte_string):
		self.port.write(0x10 | (byte_count-1))
		select.select(None, None, None, 0.1)
		for i in range(byte_count):
			self.port.write(byte_string[i])
			select.select(None, None, None, 0.1)
		bulk_read = self.port.read(byte_count)

	def low_nibble(self, nibble):
		self.port.write(0x20 | nibble)
		select.select(None, None, None, 0.1)
		return self.port.read()

	def high_nibble(self, nibble):
		self.port.write(0x30 | nibble)
		select.select(None, None, None, 0.1)
		return self.port.read()

	def cfg_pins(self, ):
		self.port.write(0x40 | )
		select.select(None, None, None, 0.1)
		if self.port.read() is 0x01: return 1
		else: return 0

	def read_pins(self):
		self.port.write(0x50)
		select.select(None, None, None, 0.1)
		return self.port.read()

	def set_speed(self, spi_speed=SPISpeed._4MHZ):
		self.port.write(0x60 | spi_speed)
		select.select(None, None, None, 0.1)
		if self.port.read() is 0x01: return 1
		else: return 0

	def read_speed(self):
		self.port.write(0x70)
		select.select(None, None, None, 0.1)
		return self.port.read()

	def cfg_spi(self, spi_cfg):
		self.port.write(0x80 | )
		select.select(None, None, None, 0.1)
		if self.port.read() is 0x01: return 1
		else: return 0

	def read_spi_cfg(self):
		self.port.write(0x90)
		select.select(None, None, None, 0.1)
		return self.port.read()

	def sleep(self):
		select.select(None, None, None, 0.1)

