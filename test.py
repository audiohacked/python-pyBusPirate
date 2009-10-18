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
import sys
from pyBusPirateLite.SPI import SPI
""" enter binary mode """
if __name__ is '__main__':
	f=open('/tmp/workfile', 'wb')
	spi = SPI("/dev/tty.usbserial-A7004qlY", 115200)
	print "Entering binmode: ",
	if spi.BBmode():
		print "OK."
	else:
		print "failed."
		sys.exit()

	print "Entering raw SPI mode: ",
	if spi.enter_SPI():
		print "OK."
	else:
		print "failed."
		sys.exit()
		
	print "Configuring SPI."
	if not spi.cfg_pins(SPIPins.POWER | SPIPins.CS):
		print "Failed to set SPI peripherals."
		sys.exit()
	if not spi.set_speed(SPISpeed._2_6MHZ):
		print "Failed to set SPI Speed."
		sys.exit()
	if not spi.cfg_spi(SPICfg.CLK_EDGE | SPICfg.OUT_TYPE):
		print "Failed to set SPI configuration.";
		sys.exit()
	spi.timeout(0.2)
	
	print "Reading EEPROM."
	spi.CS_Low()
	spi.bulk_trans(4, [0x3, 0, 0, 0])
	d = spi.bulk_trans(4)
	f.write(d)
	spi.CS_High()
	
	print "Reset Bus Pirate to user terminal: "
	if spi.resetBP():
		print "OK."
	else:
		print "failed."
		sys.exit()
		