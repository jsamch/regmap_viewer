"""
(C) 2013 MotSAI Research Inc.
Author: Alexandre Courtemanche (a.courtemanche@motsai.com)

Register Map Object
"""

import xml.etree.ElementTree as ET

eim_periph_index = 84


class RegMap(object):
	"""Register Map Object"""
	def __init__(self, svd):
		self.xmltree = ET.parse(svd)
		self.root = self.xmltree.getroot()
		periphs = self.root.find('peripherals')
		
		#Initialize lists
		self.e_reg_lists = []
		self.e_fields_lists = []
		self.periph_prefix_list = []

		#Construct lists
		for periph in periphs:
			# Construct peripheral list
			self.periph_prefix_list.append(periph.find('prependToName').text)
			print('Processing peripheral {0}'.format(periph.find('name').text))
			regs = periph.find('registers')
			reg_list = []
			field_lists = []
			'''
			for reg in regs:
				#reg_cont = list(reg)
				# Construct register names
				dim_elem = reg.find('dim')
				if(dim_elem != None): # if there multiple registers
					dim_num = int(dim_elem.text)
					for i in range(0, dim_num-1):
						reg_list.append(reg[3].text % i)
				else:
					# The name field is always the first child
					reg_list.append(reg[0].text)
				#fields = reg.find('fields')
			self.reg_lists.append(reg_list)
			'''
			for i, reg in enumerate(regs):
				#reg_cont = list(reg)
				# Construct register names
				reg_list.append(reg)

				# Get the fields in the register
				fields = reg.find('fields')
				field_list = []
				for j, field in enumerate(fields):
					field_list.append(field)
				field_lists.append(field_list)

			self.e_reg_lists.append(reg_list)
			self.e_fields_lists.append(field_lists)

	def get_periph_prefixes(self):
		return self.periph_prefix_list

	def get_reg_names(self, periph_name):
		periph_idx = self.periph_prefix_list.index(periph_name)
		#Construct register names
		reg_name_list = []
		reg_list = list(self.e_reg_lists[periph_idx])
		#print(reg_list)
		#print(reg_list)
		#print(len(reg_list))
		for i,reg in enumerate(reg_list):
			name = reg.find('name')
			dim_elem = reg.find('dim')
			if(dim_elem != None): # if there multiple registers
				dim_num = int(dim_elem.text)
				for i in range(0, dim_num-1):
					reg_name_list.append(periph_name + (reg[3].text % i))
			else:
				# The name field is always the first child
				reg_name_list.append(periph_name + reg[0].text)
			#reg_name_list.append(reg)
		return reg_name_list

	def get_reg_field(self, reg_name):
		pass		

	def reglists(self):
		return self.reg_lists
