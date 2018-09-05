#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Sean Nelson on 2018-08-19.
# Copyright 2018 Sean Nelson <audiohacked@gmail.com>
#
# This file is part of pyBusPirate.
#
# pyBusPirate is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# pyBusPirate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyBusPirate.  If not, see <https://www.gnu.org/licenses/>.

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command
from sphinx.setup_command import BuildDoc

# Package meta-data.
NAME = 'pyBusPirate'
DESCRIPTION = 'My short description for my project.'
URL = 'https://github.com/audiohacked/pyBusPirate'
EMAIL = 'audiohacked@gmail.com'
AUTHOR = 'Sean Nelson'
REQUIRES_PYTHON = '>=3.5.0'
VERSION = None

# What packages are required for this module to be executed?
REQUIRED = [
    'pyserial'
]

# What packages are optional?
EXTRAS = {
    'docs': ['sphinx'],
    'tests': ['coverage'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here,'src', 'buspirate', '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


class CoverageCommand(Command):
    """
    Support setup.py coverage.py
    """
    
    description = "Run and Report Unit Test Coverage."
    user_options = []
    
    def initialize_options(self): pass
    def finalize_options(self): pass 
    def run(self):
        import subprocess
        subprocess.call(['coverage', 'run', '-m', 'unittest', 'discover', '-v'])
        subprocess.call(['coverage', 'report', '-m'])


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='GPLv2',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    test_suite="tests",
    cmdclass={
        'upload': UploadCommand,
        'build_sphinx': BuildDoc,
        'coverage': CoverageCommand,
    },
    command_options={
            'build_sphinx': {
                'project': ('setup.py', NAME),
                'version': ('setup.py', about['__version__']),
                'release': ('setup.py', about['__version__']),
                'source_dir': ('setup.py', 'docs/source'),
                'build_dir': ('setup.py', 'docs/build'),
            }
    },
)
