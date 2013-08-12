#include <sys/mman.h>
#include <sys/time.h>
#include <err.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>

#define UART2_UTXD 0x021E8040

uint32_t read_reg(uint32_t addr);
void write_reg(uint32_t addr, uint32_t value);
void read_words(uint32_t base_addr, uint32_t* values, size_t num_words);
void write_field(uint32_t addr, uint32_t value, uint32_t width, uint32_t offset);
