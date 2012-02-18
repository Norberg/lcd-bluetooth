TARGET=attiny2313
ISP=usbasp
ISPSETTING=
SPEED = 4000000
AVRDUDE = avrdude 

COMPILE = avr-gcc -Wall -Os -mmcu=$(TARGET) -DF_CPU=$(SPEED)

OBJECTS = main.o dm_lcd.o

.c.o:
	$(COMPILE) -c $< -o $@

default:	$(OBJECTS)
	$(COMPILE) -o main.bin $(OBJECTS) -Wl,-Map,main.map
	rm -f main.hex main.eep.hex
	avr-objcopy -j .text -j .data -O ihex main.bin main.hex
burn:
	${AVRDUDE} -c ${ISP} ${ISPSETTING} -p ${TARGET}  -U flash:w:main.hex
clean:
	rm *.bin
	rm *.o
	rm *.map
	rm *.hex
	rm *.out
