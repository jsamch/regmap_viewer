
from ctypes import *

class DevMem(object):
	"""docstring for DevMem"""
	def __init__(self):
		self.dmso = cdll.LoadLibrary("./libdevmem.so")

	def read(self, addr):
		# Open file and mmap
		reg = self.dmso.read_reg(addr)
		return reg

	def write(self, addr, value):
		caddr = c_uint32(addr)
		msg = c_uint32(value)
		self.dmso.write_reg(addr, msg)

	def writefield(self, addr, value, width, offset):
		caddr = c_uint32(addr)
		cvalue = c_uint32(value)
		cwidth = c_uint32(width)
		coffset = c_uint32(offset)
		self.dmso.write_field(caddr, cvalue, cwidth, coffset)


if __name__ == '__main__':
	addr = 0x021E8094;
	dm = DevMem()
	reg = dm.read(0x021E8094)
	print("Value at {0}: {1}".format(hex(addr), hex(reg)))
	#dm.write(0x021E8040, 'e')
	
