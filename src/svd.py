"""
This file is part of PyCortexMDebug

PyCortexMDebug is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyCortexMDebug is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyCortexMDebug.  If not, see <http://www.gnu.org/licenses/>.
"""


import lxml.objectify as objectify
import sys
from copy import deepcopy
from collections import OrderedDict

class SVDFile:
	def __init__(self, fname):
		f = objectify.parse(fname)
		root = f.getroot()
		periph = root.peripherals.getchildren()
		self.peripherals = OrderedDict()
		# XML elements
		for p in periph:
			self.peripherals[str(p.name)] = SVDPeripheral(p, self)

class SVDPeripheral:
	def __init__(self, svd_elem, parent):
		self.parent = parent
		self.base_address = int(str(svd_elem.baseAddress), 0)
		try:
			derived_from = svd_elem.attrib['derivedFrom']
		except KeyError:
			# This doesn't inherit registers from anything
			self.description = str(svd_elem.description)
			self.name = str(svd_elem.name)
			self.registers = OrderedDict()
			registers = svd_elem.registers.getchildren()
			for r in registers:
				try: #Dimensioned registers
					for x in range(0, r.dim-1):
						key = str(r.name) % str(r.dimIndex.text.split(',')[x])
						self.registers[key] = SVDPeripheralRegister(r, self, x)
				except:
					self.registers[str(r.name)] = SVDPeripheralRegister(r, self)
			return
		try:
			self.name = str(svd_elem.name)
		except:
			self.name = parent.peripherals[derived_from].name
		try:
			self.description = str(svd_elem.description)
		except:
			self.description = parent.peripherals[derived_from].description
		self.registers = deepcopy(parent.peripherals[derived_from].registers)
		self.refactor_parent(parent)

	def refactor_parent(self, parent):
		self.parent = parent
		for r in self.registers.values():
			r.refactor_parent(self)
			
	def __unicode__(self):
		return str(self.name)

class SVDPeripheralRegister:
	def __init__(self, svd_elem, parent, offset = 0):
		self.parent = parent
		self.name = str(svd_elem.name)
		self.description = str(svd_elem.description)
		try:
			self.offset = int(str(svd_elem.addressOffset),0) + int(str(svd_elem.dimIncrement),0) * offset
		except AttributeError:
			self.offset = int(str(svd_elem.addressOffset),0)		

		self.size = int(str(svd_elem.size),0)

		fields = svd_elem.fields.getchildren()
		self.fields = OrderedDict()
		for f in fields:
			self.fields[str(f.name)] = SVDPeripheralRegisterField(f, self)
	
	def refactor_parent(self, parent):
		self.parent = parent
		for f in self.fields.values():
			f.refactor_parent(self)	

	def address(self):
		return self.parent.base_address + self.offset

	def get_fields(self, value):
		register_fields = []
		for field in self.fields.values():
			#print(field)

			# Mask and receive offset
			bits = (2^field.width) - 1
			mask = bits << field.offset
			#print('mask = {0} value = {1}'.format(hex(mask), (hex(value))))
			calculatedval = value & mask
			calculatedval = calculatedval >> field.offset
			field.value = calculatedval
			#print('calculatedval = {0}'.format(hex(calculatedval) ))
			try:
				evs = field.enumeratedValues.values()
				
				for ev in evs:
					if (ev.value == calculatedval):
						field.value = ev.value
						field.valuedescription = ev.description
				field_tuple = str(field.name), str(field.description), field.value, str(field.access), field.width, str(field.valuedescription)

			except AttributeError:
				field_tuple = str(field.name), str(field.description), field.value, str(field.access), field.width
				
			register_fields.append(field_tuple)
		return register_fields
	
	def __unicode__(self):
		return str(self.name)

class SVDPeripheralRegisterField:
	def __init__(self, svd_elem, parent):
		self.parent = parent
		self.name = str(svd_elem.name)
		self.description = str(svd_elem.description.text)
		self.offset = int(str(svd_elem.bitOffset))
		self.width = int(str(svd_elem.bitWidth))
		try:
			self.access = svd_elem.access
		except AttributeError:
			self.access = ''
		
		try:
			enumeratedValues = svd_elem.enumeratedValues.getchildren()
			self.enumeratedValues = OrderedDict()
			for ev in enumeratedValues:
				self.enumeratedValues[str(ev.name)] = SVDEnumeratedValue(ev, self)
		except AttributeError:
			pass

	def refactor_parent(self, parent):
		self.parent = parent
	
	def __unicode__(self):
		return str(self.name)

class SVDEnumeratedValue:
	def __init__(self, svd_elem, parent):
		self.parent = parent
		self.name = str(svd_elem.name)
		try:
			self.description = str(svd_elem.description.text)
			self.value = int(str(svd_elem.value).strip('#x'))
		except ValueError:
			self.value = -1
	
	def refactor_parent(self, parent):
		self.parent = parent

	def __unicode__(self):
		return str(self.name)

#if __name__ == '__main__':
#	svd = SVDFile(sys.argv[1])
#	print svd.peripherals['DMA1'].registers
