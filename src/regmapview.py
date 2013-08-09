"""
(C) 2013 MotSAI Research Inc.
Author: Alexandre Courtemanche (a.courtemanche@motsai.com)

Register Map Viewer
"""

import cmd
import pickle
from svd import *
from devmem import *


class RegMapViewer(cmd.Cmd, object):	
	"""Register Map Viewer interactive shell"""

	def __init__(self):
		cmd.Cmd.__init__(self)
		#self.regmap_o = RegMap('../svd/iMX6DQ.svd.xml')
		self.reset_autocomplete()
		self.verbose = False
		#self.devmem = DevMem()

	def reset_autocomplete(self):
		self.rr_num_words_in_line = 0
		self.rr_completed_prefix = False	
		self.rr_complete_reglist = []

	def autocomplete_reg(self, line):
		mline = line.partition(' ')[2] # Get the string after the first space
		prefixes = []
		for p in self.svd.peripherals.items():
			prefixes.append(p[0] + '_')
		if (mline in prefixes):
			self.rr_completed_prefix = True
			self.rr_chosen_periph_str = mline.split('_')[0]
			# Build reg list
			for reg in self.svd.peripherals[self.rr_chosen_periph_str].registers:
				self.rr_complete_reglist.append(self.rr_chosen_periph_str + '_' +reg)
			return [s for s in self.rr_complete_reglist if s.startswith(mline)]
		else:
			if self.rr_completed_prefix: # The line contains the prefix and something more
				return [s for s in self.rr_complete_reglist if s.startswith(mline)]
			else: # User has not yet completed the prefix
				return [s for s in prefixes if s.startswith(mline)]

	def do_loadregmap(self, filename):
		if filename == '':
			filename = "../svd/iMX6DQ.svd.xml"
		print('Loading '+ filename)
		self.svd = SVDFile(filename)

	def do_savepickle(self, line):
		output = open('tree.p', 'wb')
		pickle.dump(self.svd, output, pickle.HIGHEST_PROTOCOL)

	def do_loadpickle(self, line):
		inputfile = open('tree.p', 'rb')
		self.svd = pickle.load(inputfile)

	def do_readreg(self, periph_reg):
		"""Retrieves the contents of a particular register"""
		content = 0
		# Reset the autocomplete parameters
		self.reset_autocomplete()
		line = periph_reg.split('_')
		peripheral = line[0]
		register = line[1]
		addr = self.svd.peripherals[peripheral].registers[register].address()
		#content = self.devmem.read(addr)
		content = 0x00000098
		fields = self.svd.peripherals[peripheral].registers[register].get_fields(content)
		
		output_str = 'Content of register {0} at address 0x{1:08x} is 0x{2:08x}\n'.format(periph_reg, \
			(addr), (content))
		for field in fields:
			if len(field) == 6:
				output_str += "{0} ({1}) = {2:0{4}b} ({3})\n".format(field[0], field[3], field[2], field[5], field[4])
			else:
				output_str += "{0} ({1}) = {2:0{3}b}\n".format(field[0], field[3], field[2], field[4])
		print(output_str)

	def complete_readreg(self, text, line, beginidx, endidx):
		return self.autocomplete_reg(line)

	def do_writereg(self, addr, content):
		""" Set a register to a specific value"""
		output_str = 'Content of register {0} is {1}'.format(addr, content) 
		print(output_str)
		output_str = 'Content of register {0} is {1}'.format(addr, content)
		print(output_str)

	def do_map(self, hi):
		print(self.regmap_o)

	def do_addr(self, periph_reg):
		line = periph_reg.split('_')
		peripheral = line[0]
		register = line[1]
		addr = self.svd.peripherals[peripheral].registers[register].address()
		output_str = 'The address of register {0} is {1}'.format(periph_reg, hex(addr))
		print(output_str)

	def complete_addr(self, text, line, beginidx, endidx):
		return self.autocomplete_reg(line)

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