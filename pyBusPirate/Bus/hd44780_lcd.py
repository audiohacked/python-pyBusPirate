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
class LCDTypeEnum:
	"""1. HD44780 (using PCF8574 IO expander)"""
	HD44780 = 1

class MacrosLCD:
	def LCD_Reset(self):
		self.ExecMacro(1)
		
	def Init_LCD(self):
		self.ExecMacro(2)

	def Clear_LCD(self):
		self.ExecMacro(3)

	""" Cursor position ex:(4:0) """
	def CursorPos(self, pos):
		self.ExecMacro2(4)

	def WriteTestText(self):
		self.ExecMacro(5)
	
	def WriteTestNum(self, num):
		self.ExecMacro2(6, num)
	
	def WriteTestChar(self, char):
		self.ExecMacro2(7, char)
	
	def InsertText(self):
		self.ExecMacro(8)
