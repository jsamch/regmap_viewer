#include "devmem.h"

#define MMAP_BUFFER_LENGTH 1024

void write_reg(uint32_t addr, uint32_t value)
{
	int fd = -1;
	char *ptr;
	uint32_t pagesize = sysconf(_SC_PAGESIZE);

	// Open at the boundary of a page
	uint32_t page_offset = (addr % pagesize);
	uint32_t page_boundary_addr = addr - page_offset; 

	if ((fd = open("/dev/mem", O_RDWR, 0)) == -1) 
	{ 
		 err(1, "open");
	} 
	
	ptr = mmap(NULL, MMAP_BUFFER_LENGTH, PROT_WRITE | PROT_READ, MAP_SHARED, 
			 fd, page_boundary_addr); 
	 
	*(ptr + page_offset)  = value; 
	
	munmap(ptr, MMAP_BUFFER_LENGTH); 

	close(fd); 
}

uint32_t read_reg(uint32_t addr)
{
	uint32_t reg_cont = 0;
	read_words(addr, &reg_cont, 1);
	return reg_cont;
}

void read_words(uint32_t base_addr, uint32_t* values, size_t num_words)
{
	int fd = -1;
	char *ptr;
	uint32_t pagesize = sysconf(_SC_PAGESIZE);

	// Open at the boundary of a page
	uint32_t page_offset = (base_addr % pagesize);
	uint32_t page_boundary_addr = base_addr - page_offset; 
	uint32_t* reg_addr;

#if DEBUG
	printf("base_addr = %8x\n", base_addr);
	printf("page_offset = %8x\n", page_offset);
	printf("page_boundary_addr = %8x\n", page_boundary_addr);
#endif

	if ((fd = open("/dev/mem", O_RDWR, 0)) == -1)
	{
		err(1, "open");
	}
	
	ptr = mmap(NULL, MMAP_BUFFER_LENGTH, PROT_WRITE | PROT_READ, MAP_SHARED, 
			fd, page_boundary_addr);

	reg_addr = (uint32_t*) (ptr + page_offset);

#if DEBUG	
	printf("ptr = %8x\n", ptr);
	printf("page_offset = %8x\n", page_offset);
	printf("reg_addr = %8x\n", reg_addr);
#endif

	memcpy(values, reg_addr, num_words*sizeof(uint32_t));

	munmap(ptr, MMAP_BUFFER_LENGTH); 

	close(fd); 
}

void write_to_console(char character_send)
{
	write_reg(UART2_UTXD, character_send);
}

int main(int argc, char *argv[])
{
	if (argc < 2)
	{
		printf("Not enough arguments\n");
		return;
	}

	int i;
	uint32_t base_addr = strtol(argv[1], NULL, 0);
	size_t num_words = (size_t) atoi(argv[2]);
	printf("num_words = %d\nbase_addr= %08x\n", num_words, base_addr);
	
	int values[num_words];
	read_words(base_addr, values, num_words);
	for (i = 0; i < num_words; i++)
	{
		printf("Value of reg %08x is %08x\n", base_addr+(0x4*i), values[i]);
	}
}
