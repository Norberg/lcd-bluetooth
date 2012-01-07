#include <avr/io.h>
#include <util/delay.h>
#include "dm_lcd.h"

int main()
{
    lcd_init(LCD_DISP_ON);
    lcd_puts("Hello World!\n");
    lcd_puts("Bye, bye!\n");
    return 0;
}
