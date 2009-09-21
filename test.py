#!/usr/bin/python

import string
import struct
from pyBusPirate.Bus.SPI import SPI

class SPIFlash:
	def __init__(self, sp="/dev/tty.usbserial-A7004qlY", ipf=None, opf=None):
		self.IN = ipf
		self.OUT = opf
		self.spi = SPI(sp)
		self.spi.init_spi()
		self.spi.enable_spi_flash("AW")
	
	def chip_id(self, cmd=0x9f):
		s = "[0x%X r:3]\r"%cmd+""
		#print s
		self.spi.spi_send(s)

	def flash_status(self, cmd=0x5):
		s = "[0x%X r]\r"%cmd

	def flash_write(self, cmd=0xa, start=0, size=256, data=None):
		self.page_write(cmd, start, size, data)

	def flash_read(self, cmd=0x3, size=512):
		for i in range(size/256):
			d = self.page_read(start=256*i)
			self.to_file(d[7].strip('\r'))

	def page_read(self, cmd=0x3, start=0, size=256):
		s = "[0x%X 0x%X 0x%X 0x%X r:0x%X ]\r" % (cmd, start>>16&0xFF, start>>8&0xFF, start&0xFF, size) # addr
		return self.spi.spi_send(s)

	def page_write(self, cmd, start, size, data):
		if data is None: return
		s = "[6][0x%X 0x%X 0x%X 0x%X " % (cmd, start>>16&0xFF, start>>8&0xFF, start&0xFF)
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

if __name__=='__main__':
	o = open("output.bin", 'wb+')
	spi_flash = SPIFlash(opf=o)
	spi_flash.flash_read(size=256*1024)
	#spi_flash.flash_write()