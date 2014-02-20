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

class UARTCfg:
	OUTPUT_TYPE = 0x10
	DATABITS = 0x0C
	STOPBITS = 0x02
	POLARITY = 0x01

class UARTSpeed:
	_300    = 0b0000
	_1200   = 0b0001
	_2400   = 0b0010
	_4800   = 0b0011
	_9600   = 0b0100
	_19200  = 0b0101
	_33250  = 0b0110
	_38400  = 0b0111
	_57600  = 0b1000
	_115200 = 0b1001

"""
	2.1 00000000 - Exit to bitbang mode, responds "BBIOx"
	2.2 00000001 – Display mode version string, responds "ARTx"
	2.3 0000001x – Start (0)/stop(1) echo UART RX
	2.4 00000111 – Manual baud rate configuration, send 2 bytes
	2.5 00001111 - UART bridge mode (reset to exit)
	2.6 0001xxxx – Bulk UART write, send 1-16 bytes (0=1byte!)
	2.7 0100wxyz – Configure peripherals w=power, x=pullups, y=AUX, z=CS
	2.8 0110xxxx - Set UART speed
	2.9 100wxxyz – Configure UART settings
"""
class UART(BBIO):
	def __init__(self, port='/dev/ttyUSB0', speed=115200, timeout=1):
		super(UART, self).__init__(port, speed, timeout)

	def configure(self):
		if not super(UART, self).configure():
			return False
		
		if not self.enter_UART():
			return False

		return True

	def manual_speed_cfg(self, BRGH, BRGL):
		self.port.write(b"\x02")
		self.port.write(BRGH)
		self.port.write(BRGL)
		self.timeout(0.1)
		return self.response()

	def begin_input(self):
		self.port.write(b"\x04")

	def end_input(self):
		self.port.write(b"\x05")
		
	def enter_bridge_mode(self):
		self.port.write(b"\x0F")
		self.timeout(0.1)
		return self.response(1, True)
		
	def set_cfg(self, cfg):
		self.port.write(0xC0 | cfg)
		self.timeout(0.1)
		return self.response(1, True)
		
	def read_cfg(self):
		self.port.write(b"\xD0")
		self.timeout(0.1)
		return self.response(1, True)
		
	
