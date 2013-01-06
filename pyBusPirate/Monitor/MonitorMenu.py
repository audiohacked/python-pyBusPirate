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

class BusModeEnum:
	HIZ = 1
	_1WIRE = 2
	UART = 3
	I2C = 4
	SPI = 5
	JTAG = 6
	RAW2WIRE = 7
	RAW3WIRE = 8
	PC_KBD = 9
	MIDI = 10
	LCD = 11

class SpeedEnum:
	B300 = 1
	B1200 = 2
	B2400 = 3
	B4800 = 4
	B9600 = 5
	B19200 = 6
	B38400 = 7
	B57600 = 8
	B115200 = 9

class DataOutputEnum:
	HEX = 1
	DEC = 2
	BIN = 3
	RAW = 4

class OutputTypeEnum:
	OPEN_DRAIN = 1
	NORMAL = 2

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
		self.tx("F\r")

	""" Frequency generator/PWM on the AUX pin """
	def GenerateFrequency(self, freq=50, duty_cycle=50):
		self.tx("G\r")
		self.tx("%d\r"%freq)
		self.tx("%d\r"%duty_cycle)
	def SetPWM(self, freq=50, duty_cycle=50):
		self.tx("G\r")
		self.tx("%d\r"%freq)
		self.tx("%d\r"%duty_cycle)

	""" Toggle AUX control between AUX and CS/TMS pins. """
	def ToggleAUXControl(self):
		self.tx("C\r")

	""" Set bus mode (1-Wire, SPI, I2C, JTAG, UART, etc). """
	def SetBusMode(self, mode=1):
		self.tx("M\r")
		self.tx("%d\r"%mode)

	""" Set LSB/MSB first in applicable modes. """
	def SetMSB(self):
		self.tx("L\r")
		self.tx("2\r")
	def SetLSB(self):
		self.tx("L\r")
		self.tx("1\r")

	""" Pull-up resistors (V0, V2+ hardware). Power supply configuration. """
	def PullupEnable(self):
		self.tx("P\r")
		self.tx("2\r")
	def PullupDisable(self):
		self.tx("P\r")
		self.tx("1\r")

	""" Power supply voltage report (v1+ hardware only). """
	def GetPowerSupplyVal(self):
		self.tx("V\r")

	""" Hardware/firmware version information """
	def GetHWInfo(self):
		self.tx("I\r")
