#!/usr/bin/python
import sys,socket

def sendLCD(msg):
	s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
	s.connect(('localhost',3170))
	s.send(msg)
	data  = s.recv(1024)
	s.close()
	return data

def main():
	print sendLCD(sys.argv[1] + '\n')	
if __name__ == "__main__":
	main()
