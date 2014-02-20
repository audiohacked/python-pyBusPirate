#!/usr/bin/env python
# encoding: utf-8
"""
Created by Sean Nelson on 2009-10-20.
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

"""
Binary1WIRE mode:
# 00000000 - reset to BBIO
# 00000001 – mode version string (1W01)
# 00000010 – 1wire reset
# 00000100 - read byte
# 00001000 - ROM search macro (0xf0)
# 00001001 - ALARM search macro (0xec)
# 0001xxxx – Bulk transfer, send 1-16 bytes (0=1byte!)
# 0100wxyz – Configure peripherals w=power, x=pullups, y=AUX, z=CS (
# 0101wxyz – read peripherals (planned, not implemented)
"""

from .BitBang import *

class _1WIRE(BBIO):
	def __init__(self, port='/dev/ttyUSB0', speed=115200, timeout=1):
		super(_1WIRE, self).__init__(port, speed, timeout)

	def configure(self):
		if not super(_1WIRE, self).configure():
			return False
		
		if not self.enter_1wire():
			return False

		return True

	def _1wire_reset(self):
		self.port.write(b"\x02")
		self.timeout(0.1)
		return self.response(1)

	def read_byte(self):
		self.port.write(b"\x04")
		self.timeout(0.1)
		return self.response(1)

	def rom_search(self):
		self.port.write(b"\x08")
		self.timeout(0.1)
		self.__group_response()

	def alarm_search(self):
		self.port.write(b"\x09")
		self.timeout(0.1)
		self.__group_response()

	def __group_response(self):
		EOD = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
		if not self.response(): return 0
		while 1:
			data = self.port.read(8)
			if data == EOD:
				break
			print data

