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

class MonitorMenu(object):
	""" Menu Commands """
	def __init__(self):
		pass

	""" Set PC side serial port speed """
	def SetPCPortSpeed(self, speed=115200):
		pass

	""" Data Display format (DEC, HEX, BIN, or raw) """
	def DataDisplayFormat(self, format="HEX"):
		pass

	""" Measure frequency on the AUX pin """
	def MeasureFrequency(self):
		pass

	""" Frequency generator/PWM on the AUX pin """
	def GenerateFrequency(self):
		pass
	def SetPWM(self):
		pass

	""" Toggle AUX control between AUX and CS/TMS pins. """
	def ToggleAUXControl(self):
		pass

	""" Set bus mode (1-Wire, SPI, I2C, JTAG, UART, etc). """
	def SetBusMode(self, mode=1):
		pass

	""" Set LSB/MSB first in applicable modes. """
	def SetMSB(self):
		pass
	def SetLSB(self):
		pass

	""" Pull-up resistors (V0, V2+ hardware). Power supply configuration. """
	def SetPullup(self, value):
		pass

	""" Power supply voltage report (v1+ hardware only). """
	def GetPowerSupplyVal(self):
		pass

	""" Hardware/firmware version information """
	def GetHWInfo(self):
		pass
