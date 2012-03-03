TARGET=attiny2313
ISP=usbasp
ISPSETTING=
SPEED = 8000000
UART_BAUD = 9600
AVRDUDE = avrdude 

COMPILE = avr-gcc -Wall -Os -mmcu=$(TARGET) -DF_CPU=$(SPEED) -DUART_BAUD=$(UART_BAUD)

OBJECTS = main.o lib/dm_lcd.o lib/uart.o lib/uart_helper.o

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
