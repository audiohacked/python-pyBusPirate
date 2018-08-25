"""
Mock Device for Serial Devices
"""

from unittest import mock

class MockSerial(mock.MagicMock):
    def __init__(self, *args, **kwargs):
        pass

    def open(self):
        pass

    def read(self, count):
        pass
        
    def write(self, data):
        pass