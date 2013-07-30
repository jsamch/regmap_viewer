"""
(C) 2013 MotSAI Research Inc.
Author: Alexandre Courtemanche (a.courtemanche@motsai.com)

Register Map Viewer
"""

import os
import sys
import mmap
import struct
import optparse
import cmd
from regmap import *


class RegMapViewer(cmd.Cmd, object):	
	"""Register Map Viewer interactive shell"""

	def __init__(self):
		cmd.Cmd.__init__(self)
		self.regmap_o = RegMap('../svd/iMX6DQ.svd.xml')
		self.rr_num_words_in_line = 0
		self.rr_completed_prefix = False	
		self.rr_complete_reglist = []

	def do_readreg(self, addr = 0):
		"""Retrieves the contents of a particular register"""
		content = 0
		# Reset the autocomplete parameters
		self.rr_num_words_in_line = 0
		self.rr_completed_prefix = False	
		self.rr_complete_reglist = []
		output_str = 'Content of register {0} is {1}'.format(addr, content)
		print(output_str)
		#print(self.regmap_o.reglists()[84])

	def complete_readreg(self, text, line, beginidx, endidx):
		mline = line.partition(' ')[2] # Get the string after the first space
		prefixes = self.regmap_o.prefixes()

		if (mline in prefixes):
			self.rr_completed_prefix = True
			# Build reg list
			periph_index = prefixes.index(mline)
			for reg in self.regmap_o.reglists()[periph_index]:
				self.rr_complete_reglist.append(prefixes[periph_index]+reg)
			return [s for s in self.rr_complete_reglist if s.startswith(mline)]
		else:
			if self.rr_completed_prefix: # The line contains the prefix and something more
				return [s for s in self.rr_complete_reglist if s.startswith(mline)]
			else: # User has not yet completed the prefix
				return [s for s in self.regmap_o.prefixes() if s.startswith(mline)]

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

"""
	
"""