all: devmem bitmask

devmem: devmem.c
	gcc devmem.c -fpic -c -o devmem.o
	gcc -shared -o libdevmem.so devmem.o

bitmask: bitmask.c
	gcc bitmask.c -fpic -c -o bitmask.o
	gcc -shared -o libbitmask.so bitmask.o