# -*- coding: utf-8 -*-


class Writer:

	def __init__(self, device):
		self.buffer = b''

	def writeInt8(self, data):
		self.writeInt(data, 1)
        
	def writeByte(self, data):
		self.writeInt(data, 1)

	def writeInt(self, data, length=4):
		self.buffer += data.to_bytes(length, 'big')
        
	def writeLong(self, a1, a2):
		self.writeInt(a1)
		self.writeInt(a2)

	def writeVInt(self, data):

		rotate = True
		final = b''
		if data == 0:
			self.writeInt8(0)

		else:
			data = (data << 1) ^ (data >> 31)
			while data:
				b = data & 0x7f

				if data >= 0x80:
					b |= 0x80

				if rotate:

					rotate = False
					lsb = b & 0x1
					msb = (b & 0x80) >> 7
					b >>= 1
					b = b & ~(0xC0)
					b = b | (msb << 7) | (lsb << 6)

				final += b.to_bytes(1, 'big')
				data >>= 7

		self.buffer += final

	def writeString(self, data=None):
		if data is not None:
			self.writeInt(len(data))
			self.buffer += data.encode('utf-8')
		else:
			self.writeInt(2**32 - 1)

	def writeHexa(self, data):
		if data:
			if data.startswith('0x'):
				data = data[2:]

			self.buffer += bytes.fromhex(''.join(data.split()).replace('-', ''))

	def writeScID(self, class_id, instance_id):
		self.writeVInt(class_id)
		if class_id > 0:
			self.writeVInt(instance_id)
			
	def writeBool(self, boolean: bool):
		if boolean:
			self.writeInt8(1)
		else:
			self.writeInt8(0)
			
	def writeArrayVInt(self, data):
		for x in data:
			self.writeVint(x)

	def Send(self):

		self.encode()
		if hasattr(self, 'version'):
			self.device.SendData(self.id, self.buffer, self.version)

		else:
			self.device.SendData(self.id, self.buffer)
