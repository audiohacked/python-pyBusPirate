#!/usr/bin/env python
# encoding: utf-8
"""
Created by Sean Nelson on 2009-09-20.
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

from ..Monitor import MonitorCommand

class SPISpeedEnum:
	_30KHZ = 1
	_125KHZ = 2
	_250KHZ = 3
	_1MHZ = 4

class ClockPolarityEnum:
	IdleHigh = 2
	IdleLow = 1

class OutputClockEdgeEnum:
	""" Idle to Active """
	I2A = 1
	""" Active to Idle *default* """
	A2I = 2

class InputSamplePhaseEnum:
	""" Middle *default """
	MIDDLE = 1
	""" End """
	END = 2

class SPIBase(MonitorCommand):
	def __init__(self, sp='/dev/tty.usbserial-A7004qlY', speed=115200):
		MonitorCommand.__init__(self, sp, speed)

	def enable_spi_flash(self, s):
		for byte in s:
			self.tx(byte+'\r')
	
	def spi_send(self, s):
		self.conn.write(s+"\r")
		return self.lines()
	
	def spi_get(self):
		return self.rx()

	def Sniffer(self):
		self.ExecMacro(1)

class SPI(SPIBase):
	def __init__(self, p='/dev/tty.usbserial-A7004qlY', s=115200):
		SPIBase.__init__(self, p, s)
		
	def init_spi(self):
		self.SetBusMode(5)
		self.tx("4\r")
		self.tx("1\r")
		self.tx("2\r")
		self.tx("1\r")
		self.tx("2\r")

