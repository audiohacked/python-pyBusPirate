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
import time
import logging

"""
PICSPEED = 24MHZ / 16MIPS
"""

class BBException(Exception):
    pass

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
        self.logger = logging.getLogger("BusPirate")

    def configure(self):
        if not self.BBmode():
            return False

        return True

    def BBmode(self):
        """Enters bitbang dialog mode with BP
           see http://dangerousprototypes.com/docs/Bitbang
        """
        # 1 - exit from any command in standard mode
        for _ in range(10):         #10 times enter
            self.port.write(b'\r')
        self.port.flushInput()

        # 2 - standard mode reset
        self.port.write(b'#')       # BP reset

        # 3 - issue 20 times reset
        for _ in range(20):
            self.reset()

        #wait for possible response and discard
        time.sleep(0.1)
        self.port.flushInput()

        # 4 - check answers
        for _ in range(10):
            #reset
            self.reset()
            #check BBIO1 reponse
            if self.response(5) == b"BBIO1":
                return 1

        # failed :-(
        return 0

    def reset(self):
        self.port.write(b'\x00')
        #time.sleep(0.05)

    def read_mode_str(self):
        self.response(5)
        self.port.write(b"\x01")
        return self.response(4)

    def enter_SPI(self):
        self.response(5)
        self.port.write(b"\x01")
        if self.response(4) == b"SPI1": return 1
        else: return 0

    def enter_I2C(self):
        self.port.write(b"\x02")
        if self.response(4) == b"I2C1": return 1
        else: return 0

    def enter_UART(self):
        self.port.write(b"\x03")
        if self.response(4) == b"ART1": return 1
        else: return 0

    def enter_1wire(self):
        self.port.write(b"\x04")
        if self.response(4) == b"1W01": return 1
        else: return 0

    def enter_rawwire(self):
        self.port.write(b"\x05")
        if self.response(4) == b"RAW1": return 1
        else: return 0

    def resetBP(self):
        self.reset()
        self.response()
        self.port.flushInput()
        self.port.write(b'\x0f')
        resp = self.port.read(200)
        self.logger.debug('Return to normal mode response: ' + str(resp))
        return resp[-4:] == b'HiZ>'

    def raw_cfg_pins(self, config):
        self.port.write(bytearray((0x40 | config,)))
        return self.response(1,True)

    def raw_set_pins(self, config):
        self.port.write(bytearray((0x80 | config,)))
        return self.response(1,True)

    def response(self, byte_count=1, return_data=False, excp=False):
        data = self.port.read(byte_count)
        if byte_count == 1 and return_data == False:
            if data == b"\x01":
                return 1
            else:
                if excp:
                    if data:
                        raise BBException("Bus pirate processing error")
                    else:
                        raise BBException("Timeout, no answer from bus pirate")
                else:
                    return 0
        else:
            return data

    """ Self-Test """
    def short_selftest(self):
        self.port.write(b"\x10")
        return self.response(1, True)

    def long_selftest(self):
        self.port.write(b"\x11")
        return self.response(1, True)

    """ PWM """
    def setup_pwm(self):
        pass

    def clear_pwm(self):
        self.port.write(b"\x13")
        return self.reponse(1, True)

    """ Miscellanious Functions """
    def read_voltage(self):
        self.port.write(b"\x14")
        adc = self.response(2, True)
        return (adc/1024)*6.6;

    def continuous_voltage(self):
        pass

    def read_freq(self):
        self.port.write(b"\x16")
        return self.response(4, True)

    def cfg_pins(self, pins=0):
        self.port.write(bytearray((0x40 | pins,)))
        return self.response()

    def toggle_pins(self, pins=0):
        self.port.write(bytearray((0x80 | pins,)))
        return self.response()

    """ General Commands for Higher-Level Modes """
    def mode_string(self):
        self.port.write(b"\x01")
        return self.response()

    def bulk_trans(self, byte_string=None):
        # if byte_string is an int, it is a read operation
        # create a list of value of n 0 bytes, hence writing 0
        # and geting read values
        if isinstance(byte_string, int):
            byte_string = [0]*byte_string
        if byte_string == None:
            return
        if len(byte_string) > 16:
            raise BBException("Bulk transfer too big, 16 bytes max")
        self.port.write(bytearray((0x10 | (len(byte_string)-1),)))
        self.response()
        data = bytes()
        for byte in byte_string:
            self.port.write(bytearray((byte,)))
            data += self.response(1, True, False)
        return data

    def read_pins(self):
        self.port.write(b"\x50")
        return self.response(1, True)

    def set_speed(self, spi_speed=0):
        self.port.write(bytearray((0x60 | spi_speed,)))
        return self.response()

    def read_speed(self):
        self.port.write(b"\x70")
        select.select(None, None, None, 0.1)
        return self.response(1, True)


