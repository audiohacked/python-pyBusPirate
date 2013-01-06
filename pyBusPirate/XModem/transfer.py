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

from enum import ControlChar
from transmission_medium import XComm

MAXRETRANS=25

class TransMsgBlock(XComm):
	""" Message Block Format: Transmit """
	mlen = 0
	crc = -1
	packetno = 1
	tdata = ''
	tsize = 0
	
	def __init__(self):
		XComm.__init__(self)

	def transmit(self, data, size):
		self.tdata = data
		self.tsize = size
		while 1:
			for retry in range(16):
				c = self.inbyte()
				if c is 'C':
					crc = 1
					self.start_trans()
				elif c is ControlChar.NAK:
					crc = 0
					self.start_trans()
				elif c is ControlChar.CAN:
					if self.inbyte() is ControlChar.CAN:
						self.outbyte(ControlChar.ACK)
						return None
				else:
					self.outbyte(ControlChar.CAN)
					self.outbyte(ControlChar.CAN)
					self.outbyte(ControlChar.CAN)
					return None

	def start_trans(self):
		self.tsize = 128
		xbuff = ''
		xbuff[0] = SOH
		xbuff[1] = packetno
		xbuff[2] = ~packetno
		c = self.tsize - self.mlen
		if c > self.tsize: c = self.tsize
		if c >= 0:
			xbuf[3:self.tsize+3] = ''
			if c is 0: xbuff[3] = ControlChar.CTRLZ
			else:
				xbuff[3:c] = self.tdata[self.mlen:c]
				if c < self.tsize: xbuff[3+c] = ControlChar.CTRLZ
			if crc:
				ccrc = crc16(xbuff[3], self.tsize)
				xbuff[self.tsize+3] = (ccrc>>8) & 0xFF
				xbuff[self.tsize+4] = ccrc & 0xFF
			else:
				ccks = 0
				for i in range(3,self.tsize+3): ccks += xbuff[i]
				xbuff[self.tsize+3] = ccks
			
			for retry in range(MAXRETRANS):
				for i in range(self.tsize+4+crc): self.outbyte(xbuff[i])
				c = self.inbyte()
				if c is ControlChar.ACK:
					++packetno
					self.mlen += self.tsize
					return start_trans(data,size)
				elif c is ControlChar.CAN:
					if self.inbyte() == ControlChar.CAN:
						self.outbyte(ControlChar.ACK)
						return None
				elif ControlChar.NAK:
					return None
				else:
					return None
			self.outbyte(ControlChar.CAN)
			self.outbyte(ControlChar.CAN)
			self.outbyte(ControlChar.CAN)
			return None
		else:
			for retry in range(10):
				self.outbyte(ControlChar.EOT)
				c = self.inbyte()
				if c is ControlChar.ACK: break
			if c is ControlChar.ACK: return self.mlen
			else: return None
