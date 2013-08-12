#include <stdint.h>

uint32_t new_reg_value(uint32_t prev, uint32_t value, uint32_t width, uint32_t offset)
{
	// Build the mask
	uint32_t masked = 0;
	uint32_t mask = 0;
	uint32_t bits = (1 << width) - 1;
	mask = bits << offset;
	mask = ~mask;
	masked = prev & mask;

	return (masked | (value << offset));
}