import threading, serial, socket, Queue
HOST = '' 
PORT = 3170

class Bluetooth(threading.Thread):
	def __init__(self, queue, resp_queue):
		threading.Thread.__init__(self)
		self.ser = serial.Serial(port="/dev/rfcomm1",baudrate=9600,timeout=3)
		self.ser.open()
		self.queue = queue
		self.resp_queue = resp_queue
	def run(self):
		while 1:
			msg = self.queue.get()
			resp = self.send_cmd(msg)
			self.resp_queue.put(resp)
			self.queue.task_done()		
	def send_cmd(self, msg):
		if self.ser.inWaiting() > 0:
			return "Error: Old input: " + self.ser.read(self.ser.inWaiting())
		self.ser.write(msg)
		response = self.ser.readline()
		if self.ser.inWaiting() > 0:
			return "Error: Unhandled input: " + response + self.ser.read(self.ser.inWaiting())
		else:
			return response


class Handler(threading.Thread):
	def __init__(self,conn, queue, resp_queue):
		threading.Thread.__init__(self)
		self.conn = conn
		self.queue = queue
		self.resp_queue = resp_queue
	def run(self):
		try:
			print "got connection"
			input = self.conn.recv(1024)
			print "recv", input
			self.queue.put(input)
			print "waiting on response"
			resp = self.resp_queue.get()
			print "got response"
			self.conn.send(resp)
		except socket.error:
			print "socket.error"
			self.conn.close()
		finally:
			self.resp_queue.task_done()


class Server(threading.Thread): 
	def __init__(self): 
		threading.Thread.__init__(self)
		self.socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind((HOST,PORT))
		self.socket.listen(5)
		self.queue = Queue.Queue()
		self.resp_queue = Queue.Queue()
		print "going to start bluetooth stuffs"
		self.bluetooth = Bluetooth(self.queue, self.resp_queue)
		print "init bluetooth"
		self.bluetooth.start()
		print "bluetooth thread running"
	def run(self):  
		while 1:
			print "waiting on connection"
			conn,addr = self.socket.accept()
			conn.settimeout(1)
			print "got connection..."
			handler = Handler(conn, self.queue, self.resp_queue)
			handler.start()
			print "spawned handler.."
def main():
	Server().start()
	print "server started"

if __name__ == "__main__":
    main()
