"""
(C) 2013 MotSAI Research Inc.
Author: Alexandre Courtemanche (a.courtemanche@motsai.com)

Register Map Object
"""

import xml.etree.ElementTree as ET

eim_periph_index = 84


""" Create the list of peripheral prefix names"""
class RegMap(object):
	"""docstring for RegMap"""
	def __init__(self, svd):
		self.xmltree = ET.parse(svd)
		self.root = self.xmltree.getroot()
		periphs = self.root.find('peripherals')
		
		#Initialize lists
		self.reg_lists = []
		self.periph_prefix_list = []

		#Construct lists
		for periph in periphs:
			self.periph_prefix_list.append(periph.find('prependToName').text)
			print('Processing peripheral {0}'.format(periph.find('name').text))
			regs = periph.find('registers')
			reg_list = []
			for reg in regs:
				#reg_cont = list(reg)
				dim_elem = reg.find('dim')
				if(dim_elem != None): # if there multiple registers
					dim_num = int(dim_elem.text)
					for i in range(0, dim_num-1):
						reg_list.append(reg[3].text % i)
				else:
					reg_list.append(reg[0].text) # The name field is always the first child
			self.reg_lists.append(reg_list)

	def prefixes(self):
		return self.periph_prefix_list

	def reglists(self):
		return self.reg_lists
