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

"""
Each block of the transfer looks like:
<SOH><blk #><255-blk #><--128 data bytes--><cksum>
in which:
<SOH> = 01 hex
<blk #> = binary number, starts at 01 increments by 1, and wraps 0FFH to 00H (not to 01)
<255-blk #> = blk # after going thru 8080 "CMA" instr, i.e. each bit complemented
				in the 8-bit block number. Formally, this is the "ones complement".
<cksum> = the sum of the data bytes only. Toss any carry.
"""

from enum import ControlChar
from transfer import *
from receive import *

DLY_1S=1000

class MsgBlock(RecvMsgBlock, TransMsgBlock):
	def __init__(self):
		RecvMsgBlock.__init__(self)
		TransMsgBLock.__init__(self)
	
	def got_ack(self):
		response = self.inbyte(1000)
		if response is ControlChar.ACK:
			return 1
		elif response is ControlChar.NAK:
			return 0

	def got_nak(self):
		pass

	def cksum(self, data):
		r = byte(0)
		for byte in data:
			r += byte
		return r



