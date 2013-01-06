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

import serial

class Comm:
	def __init__(self, sp, speed=115200):
		self.conn = serial.Serial(sp, speed, timeout=1)

	def tx(self, s):
		#print s
		self.conn.write(s)
		self.rx('>')

	def rx(self, t='\n', e=True):
		self.conn.flush()
		string = self.conn.read(1)
		while string.find(t) == -1:
			string += self.conn.read(1)
		return string

	def lines(self):
		lines = []
		s = self.rx()
		while s.find('>') == -1:
			lines.append(s)
			s = self.rx()
		self.rx('>')
		return lines	
