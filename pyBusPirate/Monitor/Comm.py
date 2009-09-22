import serial

class Comm:
	def __init__(self, sp, speed=115200):
		self.conn = serial.Serial(sp, speed, timeout=1)

	def tx(self, s):
		#print s
		self.conn.write(s)
		self.rx('>')

	def rx(self, t='\n', e=True):
		self.conn.flush()
		string = self.conn.read(1)
		while string.find(t) == -1:
			string += self.conn.read(1)
		return string

	def lines(self):
		lines = []
		s = self.rx()
		while s.find('>') == -1:
			lines.append(s)
			s = self.rx()
		self.rx('>')
		return lines	
