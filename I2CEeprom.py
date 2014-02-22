#!/usr/bin/env python
# encoding: utf-8
"""
Created by Alex Forencich on 2014-2-19.
Copyright 2014 Alex Forencich <alex@alexforencich.com>

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
import sys
from pyBusPirate.BinaryMode.I2C import *

class I2CEeprom(I2C):
	device_address = 0xA0
	address_size = 1
	def __init__(self, port='/dev/ttyUSB0', speed=115200, timeout=1):
		super(I2CEeprom, self).__init__(port, speed, timeout)

	def configure(self):
		if not super(I2CEeprom, self).configure():
			return False

		return True

	def address2bin(self, address):
		if self.address_size > 4:
			self.address_size = 4
		if self.address_size < 1:
			self.address_size = 1

		d = []
		for i in range(self.address_size):
			d.insert(0, (address >> 8*i) & 255)

		return d

	def write(self, address, data):
		if self.address_7bit:
			da = self.device_address
		else:
			da = self.device_address & 0xFE

		d = self.address2bin(address)

		if type(data) == list:
			d.extend(data)
		else:
			d.append(data)

		self.device_write(da, d)

	def read(self, address, length = 1):
		if self.address_7bit:
			daw = self.device_address
			dar = self.device_address
		else:
			daw = self.device_address & 0xFE
			dar = self.device_address | 1

		self.device_write(daw, self.address2bin(address))
		return self.device_read(dar, length)

