#!/usr/bin/python
import sys,socket

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
	def __init__(self):
		self.socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
		self.socket.connect(('localhost', 3170))

	def send(self, msg):
		self.socket.send(msg)

	def close(self):
		self.socket.close()
	

def main():
	lcd = HD44780(16, 2)
	client = Client()
	client.send(lcd.writeline(0, sys.argv[1]))
	client.close()
if __name__ == "__main__":
	main()
