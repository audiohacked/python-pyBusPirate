#!/usr/bin/env python
# encoding: utf-8
"""
Created by Sean Nelson on 2009-10-14.
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

import select
import serial

"""
PICSPEED = 24MHZ / 16MIPS
"""

class PinCfg:
	POWER = 0x8
	PULLUPS = 0x4
	AUX = 0x2
	CS = 0x1

class BBIOPins:
	# Bits are assigned as such:
	MOSI = 0x01;
	CLK = 0x02;
	MISO = 0x04;
	CS = 0x08;
	AUX = 0x10;
	PULLUP = 0x20;
	POWER = 0x40;

class BBIO(object):
	def __init__(self, p="/dev/bus_pirate", s=115200, t=1):
		self.port = serial.Serial(p, s, timeout=t)

	def configure(self):
		if not self.BBmode():
			return False

		return True

	def BBmode(self):
		self.resetBP()
		for i in range(20): 
			self.reset()
			self.port.flushInput();
			self.reset()
			if self.response(5) == b"BBIO1": return 1
		else: return 0

	def reset(self):
		self.port.write(b"\x00")
		self.timeout(0.1)

	def read_mode_str(self):
		self.response(5)
		self.port.write(b"\x01")
		self.timeout(0.1)
		return self.response(4)

	def enter_SPI(self):
		self.response(5)
		self.port.write(b"\x01")
		self.timeout(0.1)
		if self.response(4) == b"SPI1": return 1
		else: return 0

	def enter_I2C(self):
		self.port.write(b"\x02")
		self.timeout(0.1)
		if self.response(4) == b"I2C1": return 1
		else: return 0

	def enter_UART(self):
		self.port.write(b"\x03")
		self.timeout(0.1)
		if self.response(4) == b"ART1": return 1
		else: return 0

	def enter_1wire(self):
		self.port.write(b"\x04")
		self.timeout(0.1)
		if self.response(4) == b"1W01": return 1
		else: return 0

	def enter_rawwire(self):
		self.port.write(b"\x05")
		self.timeout(0.1)
		if self.response(4) == b"RAW1": return 1
		else: return 0

	def resetBP(self):
		self.reset()
		self.port.write(b"\x0F")
		self.timeout(0.1)
		self.port.read(2000)
		self.port.flush()
		return 1

	def raw_cfg_pins(self, config):
		self.port.write(bytearray((0x40 | config,)))
		self.timeout(0.1)

	def raw_set_pins(self, config):
		self.port.write(bytearray((0x80 | config,)))
		self.timeout(0.1)

	def timeout(self, timeout=0.1):
		select.select([], [], [], timeout)

	def response(self, byte_count=1, return_data=False):
		data = self.port.read(byte_count)
		if byte_count == 1 and return_data == False:
			if data == b"\x01": return 1
			else: return 0
		else:
			return data

	""" Self-Test """
	def short_selftest(self):
		self.port.write(b"\x10")
		self.timeout(0.1)
		return self.response(1, True)

	def long_selftest(self):
		self.port.write(b"\x11")
		self.timeout(0.1)
		return self.response(1, True)

	""" PWM """
	def setup_pwm(self):
		pass

	def clear_pwm(self):
		self.port.write(b"\x13")
		self.timeout(0.1)
		return self.reponse(1, True)

	""" Miscellanious Functions """
	def read_voltage(self):
		self.port.write(b"\x14")
		self.timeout(0.1)
		adc = self.response(2, True)
		return (adc/1024)*6.6;

	def continuous_voltage(self):
		pass

	def read_freq(self):
		self.port.write(b"\x16")
		self.timeout(0.1)
		return self.response(4, True)

	def cfg_pins(self, pins=0):
		self.port.write(bytearray((0x40 | pins,)))
		self.timeout(0.1)
		return self.response()

	def toggle_pins(self, pins=0):
		self.port.write(bytearray((0x80 | pins,)))
		self.timeout(0.1)
		return self.response()

	""" General Commands for Higher-Level Modes """
	def mode_string(self):
		self.port.write(b"\x01")
		self.timeout(0.1)
		return self.response()

	def bulk_trans(self, byte_count=1, byte_string=None):
		if byte_string == None: pass
		self.port.write(bytearray((0x10 | (byte_count-1),)))
		self.timeout(0.1)
		for i in range(byte_count):
			self.port.write(bytearray((byte_string[i],)))
			self.timeout(0.1)
		data = self.response(byte_count+2, True)
		return data[1:]

	def read_pins(self):
		self.port.write(b"\x50")
		self.timeout(0.1)
		return self.response(1, True)

	def set_speed(self, spi_speed=0):
		self.port.write(bytearray((0x60 | spi_speed,)))
		self.timeout(0.1)
		return self.response()

	def read_speed(self):
		self.port.write(b"\x70")
		select.select(None, None, None, 0.1)
		return self.response(1, True)

        
