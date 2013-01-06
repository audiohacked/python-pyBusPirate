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

class RecvMsgBlock:
	""" Message Block format: Receive """
	retrans=25
	retry=0
	packetno=1
	bufsz = 0
	trychar = 'C'
	mlen = 0
	dest=''
	rfile = None
	
	def __init__(self, of=None):
		XComm.__init__(self)
		self.rfile = of

	def check(self, crc, string, size):
		if crc:
			crc = crc16(string,size)
			tcrc = (string[size]<<8)+string[size+1]
			if crc is tcrc: return 1
		else:
			cks = 0
			for i in range(size): cks += string[i]
			if cks is string[size]: return 1
		return 0

	def receive(self):
		crc = 0
		for retry in range(16):
			if self.trychar: self.outbyte(self.trychar)
			c = self.inbyte()
			if c is ControlChar.SOH:
				self.bufsz = 128
				self.start_recv()
			elif c is ControlChar.STX:
				self.bufsz = 1024
				self.start_recv()
			elif c is ControlChar.EOT:
				self.outbyte(ControlChar.ACK)
			elif c is ControlChar.CAN:
				if self.inbyte() is ControlChar.CAN: self.outbyte(ControlChar.ACK)
			else:
				if self.trychar is 'C':
					self.trychar = ControlChar.NAK
					continue
				self.outbyte(ControlChar.CAN)
				self.outbyte(ControlChar.CAN)
				self.outbyte(ControlChar.CAN)
				return None

	def start_recv(self):
		if self.trychar is 'C': crc = 1
		self.trychar = 0
		xbuff = ''
		xbuff[0] = c
		dest = ''
		for i in range(self.bufsz+crc+3):
			c = self.self.inbyte(DLY_1S)
			if not c: self.reject()
			xbuff[i] = c
		if (xbuff[1] == ~xbuff[2]) and (xbuff[1] == packetno or xbuff[1] == (packetno-1)) and 		check(crc, xbuff[3:], self.bufsz):
			if (xbuff[1] == packetno):
				count = destsz - slen
				if count > self.bufsz: count = self.bufsz
				if count > 0:
					dest += xbuff[3:count+3]
					slen += count
				++packetno
				self.retrans = MAXRETRANS+1
			if --self.retrans <= 0:
				self.outbyte(ControlChar.CAN)
				self.outbyte(ControlChar.CAN)
				self.outbyte(ControlChar.CAN)
				return -3
			self.outbyte(ControlChar.ACK)

	def reject(self):
		self.outbyte(ControlChar.NAK)

	def write_file(self):
		pass
