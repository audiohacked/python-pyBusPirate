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
import sys
import time
import base64

import serial

from pyBusPirate.BinaryMode import *

""" enter binary mode """
if __name__ == '__main__':
    reset_bp = False
    try:
        spi = SPI.SPI("/dev/ttyUSB0", 115200)
        print("Entering binmode: ")
        if spi.BBmode():
            print("OK.")
        else:
            print("failed.")
            sys.exit()

        reset_bp = True

        print("Entering raw SPI mode: ")
        if spi.enter_SPI():
            print("OK.")

        print("Configuring SPI.")
        if not spi.cfg_pins(BitBang.PinCfg.POWER | BitBang.PinCfg.CS):
            print("Failed to set SPI peripherals.")
            sys.exit()
        if not spi.set_speed(SPI.SPISpeed._2_6MHZ):
            print("Failed to set SPI Speed.")
            sys.exit()
        if not spi.cfg_spi(SPI.SPICfg.CLK_EDGE | SPI.SPICfg.OUT_TYPE):
            print("Failed to set SPI configuration.")
            sys.exit()

        time.sleep(0.2)

        print("Reading EEPROM.")
        spi.CS_Low()
        spi.bulk_trans([0x3, 0, 0, 0])
        d = spi.bulk_trans(4)
        print(base64.b16encode(d))
        spi.CS_High()

    except BitBang.BBException as excp:
        print(excp)

    except serial.SerialException as excp:
        print("Serial port issue: " + str(excp))
        reset_bp = False

    finally:
        if reset_bp:
            print("Reset Bus Pirate to user terminal: ")
            if spi.resetBP():
                print("OK.")
            else:
                print("Failed.")

