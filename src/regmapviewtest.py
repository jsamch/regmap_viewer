'''
from regmapview import *
rmv = RegMapViewer()
rmv.do_loadregmap('')
print(rmv.complete_readreg('dasf', 'readreg EI', 0, 123))
print(rmv.complete_readreg('dasf', 'readreg EIM_', 0, 123))
'''
'''
from regmapview import *
rmv = RegMapViewer()
rmv.do_loadregmap('')
rmv.complete_addr('dasf', 'addr EI', 0, 123)
print(rmv.complete_addr('dasf', 'addr EIM_', 0, 123))
'''

from regmapview import * 
rmv = RegMapViewer()
rmv.do_loadregmap('')
rmv.do_readreg('UART2_USR2')
