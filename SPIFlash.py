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

import string
import struct
from array import array
from pyBusPirate.Bus.SPI import SPI

class SPIFlash(SPI):
	wren_cmd = 0x6
	wrdi_cmd = 0x4
	rdid_cmd = 0x9f
	rdsr_cmd = 0x5
	read_cmd = 0x3
	fast_read_cmd = 0xb
	pw_cmd = 0xa
	pp_cmd = 0x2
	pe_cmd = 0xdb
	se_cmd = 0xd8
	dp_cmd = 0xb9
	rdp_cmd = 0xab
	in_data = None
	in_sdata = None
	IN = None
	OUT = None

	def b2s(self, data):
		in_sdata = array('H', data)
	
	def s2b(self, data):
		in_data = array('B', data)

	def __init__(self, sp="/dev/tty.usbserial-A7004qlY", ipf=None, opf=None):
		SPI.__init__(self, sp)
		self.IN = ipf
		self.OUT = opf
		self.spi = self
		self.spi.init_spi()
		self.spi.enable_spi_flash("AW")

	def set_cmd_codes(self, wren=0x6, wrdi=0x4, rdid=0x9f, rdsr=0x5, read=0x3,
		fast_read=0xb, pw=0xa, pp=0x2, pe=0xdb, se=0xd8, dp=0xb8, rdp=0xab ):
		self.wren_cmd = wren
		self.wrdi_cmd = wrdi
		self.rdid_cmd = rdid
		self.rdsr_cmd = rdsr
		self.read_cmd = read
		self.fast_read_cmd = fast_read
		self.pw_cmd = pw
		self.pp_cmd = pp
		self.pe_cmd = pe
		self.se_cmd = se
		self.dp_cmd = dp
		self.rdp_cmd = rdp
		
	def chip_id(self):
		s = "[0x%X r:3]\r"%self.rdid_cmd
		self.spi.spi_send(s)

	def flash_status(self):
		s = "[0x%X r]\r"%self.rdsr_cmd

	def flash_write(self, start=0, size=256, data=in_data):
		if data is None: pass
		for i in range(size/256):
			self.page_write(256*i, size, data[256*i:256*(i+1)])

	def flash_read(self, start=0, size=512):
		for i in range(size/256):
			d = self.page_read(start=256*i)
			self.to_file(d[7].strip('\r'))

	def page_read(self, start=0, size=256):
		s = "[0x%X 0x%X 0x%X 0x%X r:0x%X ]\r" % (self.read_cmd, start>>16&0xFF, start>>8&0xFF, start&0xFF, size) # addr
		return self.spi.spi_send(s)

	def page_write(self, start, size, data):
		if data is None: pass
		s = "[6][0x%X 0x%X 0x%X 0x%X " % (self.pw_cmd, start>>16&0xFF, start>>8&0xFF, start&0xFF)
		for byte in data: s += "0x%X "%byte
		s +="]\r"
		#print s
		self.spi.spi_send(s)
	
	def to_file(self, data, debug=False):
		for byte in data.split(' '):
			if debug: print byte
			try:
				h = string.atoi(byte, base=16)
				x = struct.pack("<B", h)
				self.OUT.write(x)
			except:
				continue
	
	def from_file(self, ipf=IN, size=512 debug=False):
		if ipf is not self.IN: self.IN = ipf
		self.in_data = array('B')
		self.in_data.fromfile(ipf, size)

