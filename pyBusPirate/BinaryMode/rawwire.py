#!/usr/bin/env python
# encoding: utf-8
"""
Created by Sean Nelson on 2012-06-20.
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

from .BitBang import *

class I2CSpeed:
	_400KHZ = 3
	_100KHZ = 2
	_50KHZ = 1
	_5KHZ = 0

class RawConfig:
	_w_HiZ = 0
	_w_3_3v = 8
	_x_2wire = 0
	_x_3wire = 4
	_y_MSB = 0
	_y_LSB = 2

"""

	2.1 00000000 – Exit to bitbang mode, responds “BBIOx”
	2.2 00000001 – Display mode version string, responds “RAWx”
	2.3 0000001x - I2C-style start (0) / stop (1) bit
	2.4 0000010x- CS low (0) / high (1)
	2.5 00000110 - Read byte
	2.6 00000111 - Read bit
	2.7 00001000 - Peek at input pin
	2.8 00001001 - Clock tick
	2.9 0000101x - Clock low (0) / high (1)
	2.10 0000110x - Data low (0) / high (1)
	2.11 0001xxxx – Bulk transfer, send 1-16 bytes (0=1byte!)
	2.12 0010xxxx - Bulk clock ticks, send 1-16 ticks
	2.13 0011xxxx - Bulk bits, send 1-8 bits of the next byte (0=1bit!) (added in v4.5)
	2.14 0100wxyz – Configure peripherals w=power, x=pullups, y=AUX, z=CS
	2.15 011000xx – Set speed, 3=~400kHz, 2=~100kHz, 1=~50kHz, 0=~5kHz
	2.16 1000wxyz – Config, w=HiZ/3.3v, x=2/3wire, y=msb/lsb, z=not used
	2.17 10100100 - PIC write. Send command + 2 bytes of data, read 1 byte (v5.1)
	2.18 10100101 - PIC read. Send command, read 1 byte of data (v5.1)

"""
class RawWire(BBIO):
	def __init__(self, port, speed):
		super(RawWire, self).__init__(port, speed)

	def configure(self):
		if not super(RawWire, self).configure():
			return False
		
		if not self.enter_rawwire():
			return False

		return True

	def start(self):
		pass

	def stop(self):
		pass

	def cs_low(self):
		pass

	def cs_high(self):
		pass

	def read_byte(self):
		pass

	def read_bit(self):
		pass

	def clock_tick(self):
		pass

	def clock_low(self):
		pass

	def clock_high(self):
		pass

	def data_low(self):
		pass

	def data_high(self):
		pass

	def bulk_ticks(self):
		pass

	def bulk_bits(self):
		pass

	def raw_cfg(self, cfg):
		pass

	def pic_write(self, byte_string):
		if byte_string == None: pass
		self.port.write(b"\xA4")
		self.timeout(0.1)
		for i in range(2):
			self.port.write(chr(byte_string[i]))
			self.timeout(0.1)
		data = self.response(byte_count+2, True)
		return data[1:]

	def pic_read(self):
		pass

