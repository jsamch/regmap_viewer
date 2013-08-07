#include "devmem.h"

#define MMAP_BUFFER_LENGTH 1024
#define READ_COUNT      1 
#define UART_TX_ADDR 0x021E8040

int read_reg(int addr)
{
	int i=0;
	int fd = -1;
	//int temp;
	char *anon, *zero, *ptr;
	int value = 0;
	int reg_cont = 0;
	//int write_offset = 0x40;
	int pagesize = sysconf(_SC_PAGESIZE);
	//printf("pgesize = %d", pagesize);
	// Open at the boundary of a page
	int write_offset = (addr % pagesize);
	int page_boundary_addr = addr - write_offset; 
	//printf("page_boundary = %x\n", page_boundary_addr);
	//printf("write_offset = %x\n", write_offset);
	if ((fd = open("/dev/mem", O_RDWR, 0)) == -1) 
	{
		err(1, "open"); 
	}
	
	ptr = mmap(NULL, MMAP_BUFFER_LENGTH, PROT_WRITE | PROT_READ, MAP_SHARED, 
			fd, page_boundary_addr); 
	//printf("ptr = %x\n", ptr);
	//printf("write_offset = %x\n", write_offset); 
	reg_cont = *(ptr + write_offset); 
	 
	munmap(ptr, MMAP_BUFFER_LENGTH); 

	close(fd); 

	return reg_cont;
}


int write_reg(int addr, int value)
{
	int i=0;
	int fd = -1;
	//int temp;
	char *anon, *zero, *ptr;

	int reg_cont = 0;
	//int write_offset = 0x40;
	int pagesize = sysconf(_SC_PAGESIZE);
	//printf("pgesize = %d", pagesize);
	// Open at the boundary of a page
	int write_offset = (addr % pagesize);
	int page_boundary_addr = addr - write_offset; 
	//printf("page_boundary = %x", page_boundary_addr); 
	if ((fd = open("/dev/mem", O_RDWR, 0)) == -1) 
	{ 
		 err(1, "open"); 
	} 
	
	ptr = mmap(NULL, MMAP_BUFFER_LENGTH, PROT_WRITE | PROT_READ, MAP_SHARED, 
			 fd, page_boundary_addr); 
	 
	//printf("write_offset = %x\n", write_offset); 
	*(ptr + write_offset)  = value; 
	
	munmap(ptr, MMAP_BUFFER_LENGTH); 

	close(fd); 

	return reg_cont;
}

#if 0
int main(int argc, char *argv[])
{
	/*write_reg(0x021E8040, (int) 'a');
	write_reg(0x021E8040, (int) 'l');
	write_reg(0x021E8040, (int) 'e');
	write_reg(0x021E8040, (int) 'x');
	*/
	int addr = 0x021880E4;
	printf("Reading register %x:\n", addr);
	int reg = read_reg(addr);
	printf("Value is 0x%08x\n\n", reg);
	addr = 0x021880E8;
	printf("Reading register %x:\n", addr);
	reg = read_reg(addr);
	printf("Value is 0x%08x\n\n", reg);
	addr = 0x021880EC;
	printf("Reading register %x:\n", addr);
	reg = read_reg(addr);
	printf("Value is 0x%08x\n\n", reg);
	addr = 0x021E80AC;
	printf("Reading register %x:\n", addr);
	reg = read_reg(addr);
	printf("Value is 0x%08x\n\n", reg);
}


int main(int argc, char *argv[])
{
		int i=0;
		int fd = -1;
		//int temp;
		char *anon, *zero, *ptr;
		int word_ptr;
		int word_offset = 0x84;
		int write_offset = 0x40;

		/*    
		if(argc > 0)
		{
				//printf("0x%x\n", strtol(argv[1], NULL, 0));
				//printf("%x\n", atoi(argv[0]));
		}*/

		if ((fd = open("/dev/mem", O_RDWR, 0)) == -1)
		{
			err(1, "open");
		}
		ptr = mmap(NULL, MMAP_BUFFER_LENGTH, PROT_WRITE | PROT_READ, MAP_SHARED, fd, 0x021E8000);
		//memcpy(buffer, ptr, MMAP_BUFFER_LENGTH);
		//temp = (int) buffer[i];
		word_ptr = (int)ptr;
		printf("Hello\n");
		//printf("buffer: 0x%x%x%x%x\n", ptr[i+3], ptr[i+2], ptr[i+1], ptr[i]);
		printf("ptr = %x\n", word_ptr);
		printf("ptr+1 = %x\n", word_ptr+word_offset);
		printf("*(ptr+%x) = %x%x%x%x\n",word_offset,*(ptr + word_offset), *(ptr + word_offset+1),
														*(ptr + word_offset+2), *(ptr + word_offset+3));
		*(ptr + write_offset)  = '@';
		printf("ptr = %x\n", *(ptr + write_offset));

		/*
		for ( i = 0; i < READ_COUNT; i++)
		{
				memcpy(buffer, ptr+i, sizeof(int));
				printf("buffer: 0x%x\n", buffer[i]);
		}*/

		munmap(ptr, MMAP_BUFFER_LENGTH);

		close(fd);
}
#endif