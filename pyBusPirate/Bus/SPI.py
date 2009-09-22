#!/usr/bin/env python
# encoding: utf-8
"""
SPI.py

Created by Sean Nelson on 2009-09-20.
Copyright (c) 2009 Sean Nelson. All rights reserved.
"""

from ..Monitor import MonitorCommand

class SPIBase(MonitorCommand):
	def __init__(self, sp='/dev/tty.usbserial-A7004qlY', speed=115200):
		MonitorCommand.__init__(self, sp, speed)

	def enable_spi_flash(self, s):
		for byte in s:
			self.tx(byte+'\r')
	
	def spi_send(self, s):
		self.conn.write(s+"\r")
		return self.lines()
	
	def spi_get(self):
		return self.rx()

class SPI(SPIBase):
	def __init__(self, p='/dev/tty.usbserial-A7004qlY', s=115200):
		SPIBase.__init__(self, p, s)
		
	def init_spi(self):
		self.tx("M\r")
		self.tx("5\r")
		self.tx("4\r")
		self.tx("1\r")
		self.tx("2\r")
		self.tx("1\r")
		self.tx("2\r")

