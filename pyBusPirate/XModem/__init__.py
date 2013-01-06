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
-------- 5. DATA FLOW EXAMPLE INCLUDING ERROR RECOVERY

Here is a sample of the data flow, sending a 3-block message.
It includes the two most common line hits - a garbaged block,
and an <ack> reply getting garbaged. <xx> represents the
checksum byte.

SENDER RECEIVER
times out after 10 seconds,
                        <--- <nak>
<soh> 01 FE -data- <xx> --->
                        <--- <ack>
<soh> 02 FD -data- xx   ---> (data gets line hit)
                        <--- <nak>
<soh> 02 FD -data- xx   --->
                        <--- <ack>
<soh> 03 FC -data- xx   --->
    (ack gets garbaged) <--- <ack>
<soh> 03 FC -data- xx   ---> 
                        <--- <ack>
<eot>                   --->
                        <--- <ack>

"""

__all__ = [ "message_block" ]

#class XMODEM(MSGBLK):
#	pass
