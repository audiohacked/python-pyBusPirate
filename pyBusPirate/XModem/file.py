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
---- 4A. COMMON TO BOTH SENDER AND RECEIVER:

All errors are retried 10 times. For versions running with
an operator (i.e. NOT with XMODEM), a message is typed after 10
errors asking the operator whether to "retry or quit".
Some versions of the protocol use <can>, ASCII ^X, to
cancel transmission. This was never adopted as a standard, as
having a single "abort" character makes the transmission
susceptible to false termination due to an <ack> <nak> or <soh>
being corrupted into a <can> and canceling transmission.
The protocol may be considered "receiver driven", that is,
the sender need not automatically re-transmit, although it does
in the current implementations.

---- 4B. RECEIVE PROGRAM CONSIDERATIONS:
The receiver has a 10-second timeout. It sends a <nak>
every time it times out. The receiver's first timeout, which
sends a <nak>, signals the transmitter to start. Optionally,
the receiver could send a <nak> immediately, in case the sender
was ready. This would save the initial 10 second timeout. 
However, the receiver MUST continue to timeout every 10 seconds
in case the sender wasn't ready.
Once into a receiving a block, the receiver goes into a
one-second timeout for each character and the checksum. If the
receiver wishes to <nak> a block for any reason (invalid
header, timeout receiving data), it must wait for the line to
clear. See "programming tips" for ideas
Synchronizing: If a valid block number is received, it
will be: 1) the expected one, in which case everything is fine;
or 2) a repeat of the previously received block. This should
be considered OK, and only indicates that the receivers <ack>
got glitched, and the sender re-transmitted; 3) any other block
number indicates a fatal loss of synchronization, such as the
rare case of the sender getting a line-glitch that looked like
an <ack>. Abort the transmission, sending a <can>

---- 4C. SENDING PROGRAM CONSIDERATIONS.

While waiting for transmission to begin, the sender has
only a single very long timeout, say one minute. In the
current protocol, the sender has a 10 second timeout before
retrying. I suggest NOT doing this, and letting the protocol
be completely receiver-driven. This will be compatible with
existing programs.
When the sender has no more data, it sends an <eot>, and
awaits an <ack>, resending the <eot> if it doesn't get one. 
Again, the protocol could be receiver-driven, with the sender
only having the high-level 1-minute timeout to abort.

"""
