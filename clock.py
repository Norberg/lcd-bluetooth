import send2lcd, time

class Datetime():
	def __init__(self, client, lcd):
		self.client = client
		self.lcd = lcd
	def write(self):
		d = time.strftime("%Y-%m-%d")
		t = time.strftime("%H:%M:%S")
		print d
		print t
		self.client.send(self.lcd.writeline(0,d))
		self.client.send(self.lcd.writeline(1,t))

def main():
	c = send2lcd.Client()
	l = send2lcd.HD44780(16, 2)
	d = Datetime(c, l)
	while 1:
		d.write()
		time.sleep(1)

if __name__ == "__main__":
	main()
