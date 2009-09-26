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

"""
Each block of the transfer looks like:
<SOH><blk #><255-blk #><--128 data bytes--><cksum>
in which:
<SOH> = 01 hex
<blk #> = binary number, starts at 01 increments by 1, and wraps 0FFH to 00H (not to 01)
<255-blk #> = blk # after going thru 8080 "CMA" instr, i.e. each bit complemented in the 8-bit block number. Formally, this is the "ones complement".
<cksum> = the sum of the data bytes only. Toss any carry.
"""

from enum import ControlChar
from transmission_medium import XComm

class MSGBLK(XComm):
	""" Message Block format"""
	block = str()
	def __init__(self):
		XComm.__init__(self)
	
	def cksum(self, data):
		r = byte(0)
		for byte in data:
			r += byte
		return r	

	""" Sending a File """
	def transmit(self, data, b=1 bs=128):
		if bs is 1024:
			self.block = ControlChar.STX
		elif bs is 128:
			self.block = ControlChar.SOH
		else:
			return 0
		self.block += b
		self.block += (255-b)
		self.block += data
		self.block += self.cksum(data)
		self.conn.write(self.block)
		return self.got_ack()

	def retransmit(self, block):
		self.conn.write(block)
		return self.got_ack()

	def got_ack(self):
		response = self.conn.read(1)
		if response is ControlChar.ACK:
			return 1
		elif response is ControlChar.NAK:
			return 0

	def got_nak(self):
		pass

	""" Receiving a File """	
	def receive(self):
		pass

