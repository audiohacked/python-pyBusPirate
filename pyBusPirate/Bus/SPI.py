from ..Monitor import Comm

class SPI(Comm):
	def __init__(self, sp='/dev/tty.usbserial-A7004qlY', speed=115200, autoinit=False):
		Comm.__init__(self, sp, speed)
		if autoinit is True:
			self.init_spi()

	def init_spi(self):
		self.tx("M\r")
		self.tx("5\r")
		self.tx("4\r")
		self.tx("1\r")
		self.tx("2\r")
		self.tx("1\r")
		self.tx("2\r")

	def enable_spi_flash(self, s):
		for byte in s:
			self.tx(byte+'\r')
	
	def spi_send(self, s):
		self.conn.write(s+"\r")
		return self.lines()
	
	def spi_get(self):
		return self.rx()
