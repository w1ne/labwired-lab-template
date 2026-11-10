CC = arm-none-eabi-gcc
CFLAGS = -mcpu=cortex-m0 -mthumb -g -O0 -ffreestanding -nostdlib

all: demo.elf

demo.elf: src/main.c link.ld
	$(CC) $(CFLAGS) -T link.ld src/main.c -o $@

clean:
	rm -f demo.elf

.PHONY: all clean
