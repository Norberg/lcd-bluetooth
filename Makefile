TARGET=attiny2313
ISP=ftdi
PORT=/dev/ttyUSB0
SPEED = 4000000
AVRDUDE = /home/simon/avrdude-ftdi/avrdude -C /home/simon/avrdude-ftdi/avrdude.conf 

COMPILE = avr-gcc -Wall -Os -mmcu=$(TARGET) -DF_CPU=$(SPEED)

OBJECTS = main.o dm_lcd.o

.c.o:
	$(COMPILE) -c $< -o $@

main.bin:	$(OBJECTS)
	$(COMPILE) -o main.bin $(OBJECTS) -Wl,-Map,main.map

main.hex:	main.bin
	rm -f main.hex main.eep.hex
	avr-objcopy -j .text -j .data -O ihex main.bin main.hex
burn:
	${AVRDUDE} -c ${ISP} -p ${TARGET}  -U flash:w:main.hex
