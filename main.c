#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/pgmspace.h>
#include <stdlib.h>
#include <util/delay.h>
#include "lib/dm_lcd.h"
#include "lib/uart.h"
#include "lib/uart_helper.h"
#define LINE_LENGTH 16

void init()
{
	lcd_init(LCD_DISP_ON);
	uart_init( UART_BAUD_SELECT(UART_BAUD,F_CPU) ); 
	sei(); /* Enable interupts */
}

void lcd_put_spaces(uint8_t amount)
{
	uint8_t i;
	for(i = 0; i < amount; i++)
		lcd_putc(' ');
}

char get_char()
{
	uint16_t c;
	while(1)
	{
		c = uart_getc();
		if(!uart_available(c))
			continue;
		else
			return (char)c;
	}

}
int main()
{
	uint8_t c;
	char buffer[4];
	init();
	lcd_puts_P("AVR Started\n");
	uart_puts_P("AVR started\n");
	while(1)
	{
		c = get_char();
		if(c == 0xfe)
			lcd_command(get_char());
		else
			lcd_data(c);
	}
	return 0;
}
