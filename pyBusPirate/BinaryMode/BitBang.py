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
import serial

class BBIO_pins:
	# Bits are assigned as such:
	MOSI = 0x01;
	CLK = 0x02;
	MISO = 0x04;
	CS = 0x08;
	AUX = 0x10;
	PULLUP = 0x20;
	POWER = 0x40;

class BBIO:
	def __init__(self, serial_port="/dev/tty.usbserial-A7004qlY", speed=115200):
		self.port = serial.Serial(serial_port, speed)
	
	def BBmode(self):
		for i in range(20):
			self.reset()
		if self.port.read(5) is "BBIO1": return 1
		else: return 0
		

	def reset(self):
		self.port.write("\x00")
		select.select(None, None, None, 0.1)

	def enter_SPI(self):
		self.port.write("\x01")
		select.select(None, None, None, 0.1)
		if self.port.read(4) is "SPI1": return 1
		else: return 0

	def enter_I2C(self):
		self.port.write("\x02")
		select.select(None, None, None, 0.1)
		if self.port.read(4) is "I2C1": return 1
		else: return 0

	def resetBP(self):
		self.port.write("\x0f")
		select.select(None, None, None, 0.1)

	def cfg_pins(self, config):
		self.port.write(0x40 | config)
		select.select(None, None, None, 0.1)

	def set_pins(self, pins):
		self.port.write(0x80 | config)
		select.select(None, None, None, 0.1)

	def timeout(self, timeout=0.1):
		select.select(None, None, None, timeout)

	def response(self, byte_count=1, return_data=False):
		data = self.port.read(byte_count)
		if byte_count is 1 and return_data is False:
			if data is 0x01: return 1
			else: return 0
		else:
			return data
		