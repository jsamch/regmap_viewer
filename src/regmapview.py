"""
Copyright MotSAI Research Inc.
Author: Alexandre Courtemanche (a.courtemanche@motsai.com)
"""

import os
import sys
import mmap
import struct
import optparse
import cmd

class RegMapViewer(cmd.Cmd):
	"""Register Map Viewer interactive shell"""

	def do_readreg(self, addr = 0):
		"""Retrieves the contents of a particular register"""
		content = 0
		output_str = 'Content of register {0} is {1}'.format(addr, content) 
		print(output_str)

	def do_writereg(self, addr, content):
		""" Set a register to a specific value"""
		output_str = 'Content of register {0} is {1}'.format(addr, content) 
		print(output_str)
		output_str = 'Content of register {0} is {1}'.format(addr, content)
		print(output_str)

	def do_rp(self, periph):
		self.do_readperiph(periph)

	def do_readperiph(self, periph):
		"""Retrieves the contents of a particular peripheral"""
		content = 0
		output_str = 'Content of peripheral {0} is {1}'.format(periph, content) 

	def do_getfield(self, register, field):
		"""Retrieves the contents of a particular field"""
		content = 0
		output_str = 'Content of field {0} of register {1} is {2}'.format(register, field, content)
		print(output_str)

	def do_setfield(self, register, field, bits):
		""" Set the field of a particular register to a specific value"""
		content = 0
		output_str = 'Content of field {0} of register {1} is {2} before writing is'.format(register, field, content)
		print(output_str)
		output_str = 'Content of field {0} of register {1} is {2} after writing is'.format(register, field, bits)
		print(output_str)

	def do_exit(self, line):
		"""Exits the program"""
		return True
	def do_quit(self, line):
		"""Quits the program"""
		return True


if __name__ ==  '__main__':
	RegMapViewer().cmdloop()