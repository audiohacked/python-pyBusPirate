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
Asynchronous, 8 data bits, no parity, one stop bit.

The protocol imposes no restrictions on the contents of the
data being transmitted. No control characters are looked for
in the 128-byte data messages. Absolutely any kind of data may
be sent - binary, ASCII, etc. The protocol has not formally
been adopted to a 7-bit environment for the transmission of
ASCII-only (or unpacked-hex) data , although it could be simply
by having both ends agree to AND the protocol-dependent data
with 7F hex before validating it. I specifically am referring
to the checksum, and the block numbers and their ones-
complement.

"""

from ..Monitor.Comm import Comm
from enum import ControlChar

class XComm(Comm):
	def __init__(self, port="/dev/tty.usbserial-A7004qlY"):
		Comm.__init__(self, port, speed=115200)
		
	def ack(self):
		self.conn.write(ControlChar.ACK)

	def nak(self):
		self.conn.write(ControlChar.NAK)

	def can(self):
		self.conn.write(ControlChar.CAN)

	def inbyte(self, timeout=1000): # timeout in ms
		return self.conn.read(1)

	def outbyte(self, byte):
		self.conn.write(byte)

