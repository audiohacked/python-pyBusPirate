from array import array

def crc16(string, v=0):
	""" Single-function interface, like gzip module's crc32
	"""
	s = array('H', string)
	for b in s:
		v = table[ (b^v) & 0xff] ^ (v >> 8)
	return v

# CRC-16 poly: p(x) = x**16 + x**15 + x**2 + 1
# top bit implicit, reflected

#if __name__ == '__main__':
poly = 0xa001
table = array('H')
for byte in range(256):
     crc = 0
     for bit in range(8):
         if (byte ^ crc) & 1:
             crc = (crc >> 1) ^ poly
         else:
             crc >>= 1
         byte >>= 1
     table.append(crc)

#crc = CRC16()
#crc.update("123456789")
#assert crc.checksum() == '\xbb\x3d'

