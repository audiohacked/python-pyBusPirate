#!/usr/bin/env python
# encoding: utf-8
"""
Created by Sean Nelson on 2009-10-14.
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

from .BitBang import BBIO

class I2CSpeed:
	_50KHZ = 0b000
	_5KHZ = 0b001

class I2CPins:
	POWER = 0x8
	PULLUPS = 0x4
	AUX = 0x2
	CS = 0x1
	
class I2C(BBIO):
	bulk_read = None
	def __init__(self, port, speed):
		BBIO.__init__(self, port, speed)

	def send_start_bit(self):
		self.port.write("\x02")
		self.timeout(0.1)
		return self.response()
	
	def send_stop_bit(self):
		self.port.write("\x03")
		self.timeout(0.1)
		return self.response()
		
	def read_byte(self):
		self.port.write("\x04")
		self.timeout(0.1)
		return self.response(1, True)
		
	def send_ack(self):
		self.port.write("\x06")
		self.timeout(0.1)
		return self.response()
		
	def send_nack(self):
		self.port.write("\x07")
		self.timeout(0.1)
		return self.response()

