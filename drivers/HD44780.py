#encoding:utf-8

class HD44780:
	char_mapping = {'å':'a',
	                'ä':'a', #225
			'ö':'o', #239
			'Å':'A',
			'Ä':'A',
			'Ö':'O'}

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
		text = self.map_chars(text)
		data += text.ljust(self.cols) #pad string with spaces to clear all cols
		return data
	
	def map_chars(self, text):
		mapped_text = ""
		text = text.decode("utf8")
		for char in text:
			if self.char_mapping.has_key(char.encode("utf8")): 
				mapped_text += self.char_mapping[char.encode("utf8")]
			else:
				mapped_text += char
		return mapped_text.encode("utf8")
	
	def clear(self):
		return self.command(0x01)

	def blank(self):
		return self.command(0x08)
	
	def restore(self):
		return self.command(0x0c)
