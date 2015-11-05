#!/usr/bin/env python
# encoding: utf-8
"""
Created by Sean Nelson on 2013-01-06.
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

from distutils.core import setup

setup(
	name = "pyBusPirate",
	version = "0.9.2.0",
	author = "Sean Nelson",
	author_email = "audiohacked@gmail.com",
	description = ("pyBusPirate is a library to use/control the Dangerous"
					"Prototypes' Bus Pirate."),
	license = "GPLv3",
	url = "https://gitorious.org/audiohacked/pybuspirate",
	packages=['pyBusPirate',
			'pyBusPirate.BinaryMode',
			'pyBusPirate.Bus',
			'pyBusPirate.Monitor',
			'pyBusPirate.XModem'],
)

