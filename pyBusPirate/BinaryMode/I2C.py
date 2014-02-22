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

from .BitBang import BBIO

class I2CSpeed:
	_400KHZ = 3
	_100KHZ = 2
	_50KHZ = 1
	_5KHZ = 0

class I2CPins:
	POWER = 0x8
	PULLUPS = 0x4
	AUX = 0x2
	CS = 0x1

class I2C(BBIO):
	bulk_read = None
	address_7bit = False
	def __init__(self, port='/dev/ttyUSB0', speed=115200, timeout=1):
		super(I2C, self).__init__(port, speed, timeout)

	def configure(self):
		if not super(I2C, self).configure():
			return False
		
		if not self.enter_I2C():
			return False

		return True

	def send_start_bit(self):
		self.port.write(b"\x02")
		self.timeout(0.1)
		return self.response()

	def send_stop_bit(self):
		self.port.write(b"\x03")
		self.timeout(0.1)
		return self.response()

	def read_byte(self):
		self.port.write(b"\x04")
		self.timeout(0.1)
		return self.response(1, True)

	def send_ack(self):
		self.port.write(b"\x06")
		self.timeout(0.1)
		return self.response()

	def send_nack(self):
		self.port.write(b"\x07")
		self.timeout(0.1)
		return self.response()

	def start_sniffer(self):
		self.port.write(b"\x0F")
		self.timeout(0.1)

	def ext_AUX(self, cmd):
		self.port.write(b"\x09")
		self.timeout(0.1)
		self.port.write(cmd)
		self.timeout(0.1)
		return self.response()

	""" High level commands """
	def device_write(self, address, data):
		if self.address_7bit:
			d = [address << 1]
		else:
			d = [address]
		
		if type(data) == list:
			d.extend(data)
		else:
			d.append(data)

		self.send_start_bit()
		self.bulk_trans(len(d), d)
		self.send_stop_bit()

	def device_read(self, address, length = 1):
		if self.address_7bit:
			address = (address << 1) | 1

		d = []

		self.send_start_bit()
		self.bulk_trans(1, [address])
		while True:
			d.append(self.read_byte())
			if len(d) < length:
				self.send_ack()
			else:
				self.send_nack()
				break

		self.send_stop_bit()

		return d



