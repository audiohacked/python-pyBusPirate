#!/usr/bin/env python
# encoding: utf-8

import serial
from pyBusPirate.BinaryMode import *

bbio = BitBang.BBIO("/dev/ttyUSB0", 115200)
print("Entering binmode: ")
if bbio.BBmode():
    print("OK.")
else:
    print("Failed.")
    exit(-1)

print(bbio.resetBP())
