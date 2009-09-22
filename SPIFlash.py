#!/usr/bin/env python
# encoding: utf-8
"""
SPIFlash.py

Created by Sean Nelson on 2009-09-20.
Copyright (c) 2009 Sean Nelson. All rights reserved.
"""

import string
import struct
from pyBusPirate.Bus.SPI import SPI

class SPIFlash:
	self.wren_cmd = 0x6
	self.wrdi_cmd = 0x4
	self.rdid_cmd = 0x9f
	self.rdsr_cmd = 0x5
	self.read_cmd = 0x3
	self.fast_read_cmd = 0xb
	self.pw_cmd = 0xa
	self.pp_cmd = 0x2
	self.pe_cmd = 0xdb
	self.se_cmd = 0xd8
	self.dp_cmd = 0xb9
	self.rdp_cmd = 0xab
	self.in_data = None

	def __init__(self, sp="/dev/tty.usbserial-A7004qlY", ipf=None, opf=None):
		self.IN = ipf
		self.OUT = opf
		self.spi = SPI(sp)
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
		#print s
		self.spi.spi_send(s)

	def flash_status(self):
		s = "[0x%X r]\r"%self.rdsr_cmd

	def flash_write(self, start=0, size=256, data=self.in_data):
		if data is None: pass
		self.page_write(cmd, start, size, data)

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
		for byte in data: s += "0x"+byte.encode('hex')+" "
		s +="]\r"
		print s
		#self.spi.spi_send(s)
	
	def to_file(self, data, debug=False):
		for byte in data.split(' '):
			if debug: print byte
			try:
				h = string.atoi(byte, base=16)
				x = struct.pack("<B", h)
				self.OUT.write(x)
			except:
				continue
	
	def from_file(self, ipf=self.IN, debug=False):
		if ipf is not self.IN: self.IN = ipf
		self.in_data = []
		byte = ipf.read(1)
		while byte:
			self.in_data.append(byte)
			byte = ipf.read(1)

