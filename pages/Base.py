import sys,socket, time, threading

class Page:
	def __init__(self, display):
		#How often should this paged be refreshed
		self.freq = None
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

	def update(self):
		pass

	
class Pages:
	def __init__(self):
		self.cur_page = -1
		self.pages = list()

	def add_page(self, page):
		self.pages.append(page)
	
	def current_page(self):
		return self.pages[self.cur_page]
	
	def write_current_page(self):
		return self.current_page().write_page()

	def next_page(self):
		self.cur_page += 1
		if self.cur_page == len(self.pages):
			self.cur_page = 0
		return self.write_current_page()

class PageScheduler():
	def __init__(self, client, pages, switch_time = 5):
		self.client = client
		self.pages = pages
		self.switch_time = switch_time
			
	def run(self):
		while 1:	
			self.switch_page()			

	def switch_page(self):
		self.pages.next_page()
		t = time.time()
		freq = self.pages.current_page().freq;
		while time.time() < t + self.switch_time:
			self.update_page()
			self.client.send(self.pages.write_current_page())
			if freq is None:
				time.sleep(self.switch_time)
			else:
				time.sleep(freq)

	def update_page(self):
		self.pages.current_page().update()
