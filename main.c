#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/pgmspace.h>
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

int main()
{
	char buffer [LINE_LENGTH];
	uint8_t len;
	init();
	lcd_puts_P("AVR Started\n");
	uart_puts_P("AVR started\n");
	while(1)
	{
		len = readline(buffer, LINE_LENGTH);
		uart_puts_P("Recived: ");
		uart_puts(buffer);
		lcd_puts(buffer);
		lcd_put_spaces(LINE_LENGTH - len);	
		lcd_putc('\n');	
	}
	lcd_puts_P("Bye, bye!\n");
	return 0;
}
