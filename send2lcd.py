#!/usr/bin/python
import sys, time
from pages import Base
from Client import Client
from drivers import HD44780
	
def main():
	lcd = HD44780.HD44780(16, 2)
	client = Client()
	client.send(lcd.writeline(0, sys.argv[1]))
	client.close()

if __name__ == "__main__":
	main()
