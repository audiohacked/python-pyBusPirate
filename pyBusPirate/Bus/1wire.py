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

class Macros1Wire:
	def __init__(self):
		pass
	
	""" READ ROM (0x33) *for single device bus """
	def READ_ROM(self):
		self.ExecMacro(51)
	
	""" MATCH ROM (0x55) *followed by 64bit address """
	def MATCH_ROM(self):
		self.ExecMacro(85)
		
	""" SKIP ROM (0xCC) *followed by command """
	def SKIP_ROM(self):
		self.ExecMacro(204)
		
	""" ALARM SEARCH (0xEC) """
	def ALARM_SEARCH(self):
		self.ExecMacro(236)
		
	""" SEARCH ROM (0xF0) """
	def SEARCH_ROM(self):
		self.ExecMacro(240)

class _1Wire:
	def __init__(self):
		pass
	
	def Setup(self):
		self.SetBusMode(2)
