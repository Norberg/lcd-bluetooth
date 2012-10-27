import threading, serial, socket, Queue
HOST = '' 
PORT = 3170

class Bluetooth(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.init_serial()
		self.queue = queue

	def init_serial(self):
		self.ser = serial.Serial(port="/dev/rfcomm0",baudrate=9600,timeout=3)
		self.ser.open()

	def run(self):
		while 1:
			try:
				msg = self.queue.get()
				print "sending...", msg, "to bluetooth" 
				self.send(msg)
			except Exception as e:
				print "exception when sending to bluetooth:", e
				print "trying to recreate connection.."
				self.ser.close()
				self.ser.open()
				print "connection recreated.."
			finally:
				self.queue.task_done()

	def send(self, msg):
		self.ser.write(msg)
		if self.ser.inWaiting() > 0:
			print "Error: " + self.ser.read(self.ser.inWaiting())




class Handler(threading.Thread):
	def __init__(self, conn, queue):
		threading.Thread.__init__(self)
		self.conn = conn
		self.conn.setblocking(1)
		self.queue = queue
	def run(self):
		try:
			print "got connection"
			while 1:
				input = self.conn.recv(1024)
				if not input:
					break
				print "recv", input
				self.queue.put(input)
		except socket.error as e:
			print "socket.error:", e
		finally:
			self.conn.close()


class Server(threading.Thread): 
	def __init__(self): 
		threading.Thread.__init__(self)
		self.socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind((HOST,PORT))
		self.socket.listen(5)
		self.queue = Queue.Queue()
		print "going to start bluetooth stuffs"
		self.bluetooth = Bluetooth(self.queue)
		print "init bluetooth"
		self.bluetooth.start()
		print "bluetooth thread running"
	def run(self):  
		while 1:
			print "waiting on connection"
			conn,addr = self.socket.accept()
			conn.settimeout(1)
			print "got connection..."
			handler = Handler(conn, self.queue)
			handler.start()
			print "spawned handler.."
def main():
	Server().start()
	print "server started"

if __name__ == "__main__":
    main()
