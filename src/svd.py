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
		self.flag = False
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
					#print('r.dim = {0} r.dimIndex = {1}'.format( str(r.dim), r.dimIndex[x].split[',']))
					#print('Dimensioned register: ' + str(r.dim))
					self.flag = True
					#print('hi')
					#print( r.dimIndex.text)
					#print( r.dimIndex.text.split(','))
					#print( r.dimIndex.text.split(',')[0])
					#print( r.dimIndex.text.split(',')[1])
					#print(dimIndex)
					for x in xrange(0, r.dim-1):
						key = str(r.name) % str(r.dimIndex.text.split(',')[x])
						self.registers[key] = SVDPeripheralRegister(r, self, x)
						#print('r.name = %s + r.dimIndex[%d] = %s = ', str(r.name), x, str(r.name) % str(r.dimIndex[x]))
						#print('r.name = {0} + r.dimIndex[{1}] = {2} '.format(str(r.name), x, str(r.name) % str(r.dimIndex[x])))
				except:
					#print(str(r.name))
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
		for r in self.registers.itervalues():
			r.refactor_parent(self)
			
	def __unicode__(self):
		return str(self.name)

class SVDPeripheralRegister:
	def __init__(self, svd_elem, parent, offset = 0):
		self.parent = parent
		self.name = str(svd_elem.name)
		self.description = str(svd_elem.description)
		#self.dimi = None
		try:
			self.offset = int(str(svd_elem.addressOffset),0) + int(str(svd_elem.dimIncrement),0) * offset
		except :
			self.offset = int(str(svd_elem.addressOffset),0)		

		#self.offset = int(str(svd_elem.addressOffset),0)
		self.size = int(str(svd_elem.size),0)

		fields = svd_elem.fields.getchildren()
		self.fields = OrderedDict()
		for f in fields:
			self.fields[str(f.name)] = SVDPeripheralRegisterField(f, self)
	
	def refactor_parent(self, parent):
		self.parent = parent
		for f in self.fields.itervalues():
			f.refactor_parent(self)
		

	def address(self):
		return self.parent.base_address + self.offset
	
	def __unicode__(self):
		return str(self.name)

class SVDPeripheralRegisterField:
	def __init__(self, svd_elem, parent):
		self.parent = parent
		self.name = str(svd_elem.name)
		self.description = str(svd_elem.description)
		self.offset = int(str(svd_elem.bitOffset))
		self.width = int(str(svd_elem.bitWidth))
		try:
			self.access = svd_elem.access
		except AttributeError:
			self.access = ''

	def refactor_parent(self, parent):
		self.parent = parent
	
	def __unicode__(self):
		return str(self.name)

#if __name__ == '__main__':
#	svd = SVDFile(sys.argv[1])
#	print svd.peripherals['DMA1'].registers
