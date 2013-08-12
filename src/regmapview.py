"""
(C) 2013 MotSAI Research Inc.
Author: Alexandre Courtemanche (a.courtemanche@motsai.com)

Register Map Viewer
"""

import cmd
import pickle
from svd import *
from devmem import *
from ctypes import *


class RegMapViewer(cmd.Cmd, object):	
	"""Register Map Viewer interactive shell"""

	def __init__(self):
		cmd.Cmd.__init__(self)
		#self.regmap_o = RegMap('../svd/iMX6DQ.svd.xml')
		self.reset_autocomplete()
		self.verbose = False
		self.devmem = DevMem()

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
		content = self.devmem.read(addr)
		#content = 0x00000098
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

	def do_writereg(self, periph_reg_content):
		""" Set a register to a specific value"""
		# Reset the autocomplete parameters
		self.reset_autocomplete()
		line = periph_reg_content.split(' ')
		periph_reg = line[0].split('_')
		peripheral = periph_reg[0]
		register = periph_reg[1]
		content = int(line[1][0])
		addr = self.svd.peripherals[peripheral].registers[register].address()
		beforecontent = self.devmem.read(addr)
		output_str = 'Before write: content of {0} is {1:08x}'.format(addr, beforecontent)
		print(output_str)
		self.devmem.write(addr, content)
		output_str = 'After write: content of register {0} is {1:08x}'.format(addr, content)
		print(output_str)

	def complete_writereg(self, text, line, beginidx, endidx):
		return self.autocomplete_reg(line);

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

	def do_writefield(self, periph_reg_field_content):
		""" Set a register field to a specific value"""
		# Reset the autocomplete parameters
		self.reset_autocomplete()
		line = periph_reg_field_content.split(' ')
		periph_reg = line[0].split('_')
		peripheral_str = periph_reg[0]
		register_str = periph_reg[1]
		field_str = line[1]
		newbits = int(line[2], 2) # Intepret as binary
		register = self.svd.peripherals[peripheral_str].registers[register_str]
		field = register.fields[field_str]
		addr = register.address()
		prevvalue = self.devmem.read(addr)
		#prevvalue = 0x0000002A
		# Get the new value
		self.devmem.writefield(addr, newbits, field.width, field.offset)

		output_str = 'Before write: content of {0} is {1:08x}'.format(register_str, prevvalue)
		print(output_str)
		newvalue = self.devmem.read(addr)
		output_str = 'After write: content of {0} is {1:08x}'.format(register_str, newvalue)
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