#!/usr/bin/python
import time
from pages import Base
from pages import Clock
from pages import Temperature
from Client import Client
from drivers import HD44780
	
def main():
	page1 = Temperature.Temperature(HD44780.HD44780(16,2))
	page2 = Clock.Clock(HD44780.HD44780(16,2))
	pages = Base.Pages()
	pages.add_page(page1)
	pages.add_page(page2)
	client = Client("atom")
	sched = Base.PageScheduler(client, pages, 5)
	sched.run()

if __name__ == "__main__":
	main()
