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
class MonitorSyntax:
	""" Class for Monitor Syntax Switches """
	def __init__(self):
		pass

	""" Toggle Auxiliary pin"""
	def AuxHigh(self):
		self.tx("A\r")
	def AuxLow(self):
		self.tx("a\r")
	def AuxHiZ(self):
		self.tx("@\r")

	""" Enable/Disable on-board power supplies """
	def EnablePower(self):
		self.tx("W\r")
	def DisablePower(self):
		self.tx("w\r")

	""" Delay 1uS """
	def Delay1us(self):
		self.tx("&\r")

	""" Macros """
	def ExecMacro(self, macro):
		self.tx("(%d)\r"%macro)
	def ExecMacro2(self, macro, n):
		self.tx("(%d:%d)\r"%(macro, n))

	""" Measure voltage on ADC pin """
	def MeasureVoltage(self):
		self.tx("D\r")

	""" Read byte """
	def ReadByte(self, count=1):
		self.tx("R\r")
		
