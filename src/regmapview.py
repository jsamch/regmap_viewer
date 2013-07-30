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
import cPickle as pickle
from regmap import *


class RegMapViewer(cmd.Cmd, object):	
	"""Register Map Viewer interactive shell"""

	def __init__(self):
		cmd.Cmd.__init__(self)
		#self.regmap_o = RegMap('../svd/iMX6DQ.svd.xml')
		self.reset_autocomplete()

	def reset_autocomplete(self):
		self.rr_num_words_in_line = 0
		self.rr_completed_prefix = False	
		self.rr_complete_reglist = []
		self.rr_periph_index = None

	def do_createregmap(self, dumpfile= './iMX6DQ.p', svd = '../svd/iMX6DQ.svd.xml'):
		print('Parsing file')
		rm = RegMap(svd)
		print('Serializing...')
		pickle.dump( rm, open('./iMX6DQ.p', 'wb'))
		print('Saved to file '+ dumpfile)

	def do_loadregmap(self, filename):
		self.reset_autocomplete()
		print('Loading '+ filename)
		self.regmap_o = pickle.load(open('iMX6DQ.p', 'rb'))

	def do_readreg(self, addr = 0):
		"""Retrieves the contents of a particular register"""
		content = 0
		# Reset the autocomplete parameters
		self.reset_autocomplete()
		output_str = 'Content of register {0} is {1}'.format(addr, content)
		print(output_str)
		#print(self.regmap_o.reglists()[84])

	def complete_readreg(self, text, line, beginidx, endidx):
		mline = line.partition(' ')[2] # Get the string after the first space
		prefixes = self.regmap_o.prefixes()
		autocomplete_list = []
		mylist = ['SATA_', 'zvc', 'qwer']
		'''
		print('hi')
		print(prefixes)
		print(mline)
		print(self.rr_periph_index)
		print('mline.startswith(prefixes(self.rr_periph_index) = '+ mline.startswith(prefixes(self.rr_periph_index)))
		'''
		if (mline in prefixes):
			# Build reg list
			#self.rr_periph_index = prefixes.index(mline)
			print('hi')
			print('prefixes.index(mline)' + mylist.index(mline))
			#for reg in self.regmap_o.reglists()[self.rr_periph_index]:
			#	self.rr_complete_reglist.append(prefixes[self.rr_periph_index]+reg)
			#return [s for s in self.rr_complete_reglist if s.startswith(mline)]
			return [s for s in prefixes if s.startswith(mline)]
		else:
			return [s for s in prefixes if s.startswith(mline)]

		'''
		# Completed the prefix
		if (mline in prefixes):
			# Build reg list
			print('1')
			self.rr_periph_index = prefixes.index(mline)
			for reg in self.regmap_o.reglists()[self.rr_periph_index]:
				self.rr_complete_reglist.append(prefixes[self.rr_periph_index]+reg)
			return [s for s in self.rr_complete_reglist if s.startswith(mline)]
		# Changed prefix
		elif self.rr_periph_index is None:
			print('2')
			return [s for s in prefixes if s.startswith(mline)]
		elif mline.startswith(prefixes(self.rr_periph_index)):
			print('3')
			return [s for s in self.rr_complete_reglist if s.startswith(mline)]
		else: # User has not yet completed the prefix
			print('4')
			self.rr_periph_index = None
			return [s for s in prefixes if s.startswith(mline)]
		return autocomplete_list
		'''


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

