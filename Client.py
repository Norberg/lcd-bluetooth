import socket

class Client:
	def __init__(self, host = "localhost", port = 3170):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((host, port))
	
	def send(self, msg):
		self.socket.send(msg)

	def close(self):
		self.socket.close()
	
