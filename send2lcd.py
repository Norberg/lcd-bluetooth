#!/usr/bin/python
import sys,socket, time, threading

class HD44780:
	def __init__(self, cols, rows):
		self.cols = cols
		self.rows = rows
		self.cur_pos = (0,0)
		self.line = [0x80, 0xc0, 0x94, 0xd4]
	def command(self,command):	
		return chr(0xfe)+chr(command)

	def data(self, data):
		return chr(data)
	
	def change_pos(self, col, row):
		return self.command(self.line[col]+row)

	def writeline(self, line, text):
		data = self.change_pos(line, 0)
		data += text.ljust(self.cols) #pad string with spaces to clear all cols
		return data
	
	def clear(self):
		return self.command(0x01)

	def blank(self):
		return self.command(0x08)
	
	def restore(self):
		return self.command(0x0c)
	

class Client:
	def __init__(self, host = "localhost", port = 3170):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((host, port))
	
	def send(self, msg):
		self.socket.send(msg)

	def close(self):
		self.socket.close()
	
class Page:
	def __init__(self, display):
		self.display = display
		self.lines = list()
		for i in range(self.display.rows):
			self.lines.append("")

	def setline(self, line, text):
		self.lines[line] = text

	def write_page(self):
		data = ""
		for i in range(self.display.rows):
			data += self.display.writeline(i, self.lines[i])
		return data
class Pages:
	def __init__(self):
		self.current_page = -1
		self.pages = list()

	def add_page(self, page):
		self.pages.append(page)
	
	def write_current_page(self):
		return self.pages[self.current_page].write_page()

	def next_page(self):
		self.current_page += 1
		if self.current_page == len(self.pages):
			self.current_page = 0
		return self.write_current_page()

class PageScheduler(threading.Thread):
	def __init__(self, client, pages, switch_time = 5):
		threading.Thread.__init__(self)
		self.client = client
		self.pages = pages
		self.switch_time = switch_time
			
	def run(self):
		while 1:
			self.client.send(self.pages.next_page())
			time.sleep(self.switch_time)
		self.client.close()


def main():
	lcd = HD44780(16, 2)
	client = Client()
	client.send(lcd.writeline(0, sys.argv[1]))
	client.close()



def demo():
	page1 = Page(HD44780(16,2))
	page2 = Page(HD44780(16,2))
	page1.setline(0,"Indoor: 24.3C")	
	page1.setline(1,"Outdoor: 8.5C")
	page2.setline(0,"Klockan ar:")
	t = time.strftime("%H:%M:%S")
	page2.setline(1,t)
	pages = Pages()
	pages.add_page(page1)
	pages.add_page(page2)
	client = Client("atom")
	sched = PageScheduler(client, pages, 5)
	sched.start()
	while 1:
		t = time.strftime("%H:%M:%S")
		page2.setline(1,t)
		client.send(pages.write_current_page())
		time.sleep(1)

if __name__ == "__main__":
	demo()
