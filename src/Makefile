all: devmem regplay

devmem: devmem.c
	gcc devmem.c -fpic -c -o devmem.o
	gcc -shared -o libdevmem.so devmem.o

regplay: devmem.c
	gcc devmem.c -o regplay