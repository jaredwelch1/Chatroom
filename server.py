import socket
import sys
from _thread import *
import json

def threaded_exit_handler(self, conn):
	conn.send(str.encode('close_client'))
	

def threaded_client_handler(self, conn):
	self.num_threads += 1
	print(str(self.num_threads))
	conn.send(str.encode('Welcome, please log in using <login> <user> <pass>'))


	while True:
		data = conn.recv(2048).decode('utf-8')
		if not data:
				break
		print(str(data))
	self.num_threads -= 1
	print(str(self.num_threads))
	conn.close()


class server(object):

	def __init__(self, host='127.0.0.1', port=5555):

		try:
			with open('users.json', 'r') as file:
				self.users = json.load(file)
		except:
			print('error opening user file')
			exit()

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s = self.s
		try:
			s.bind((host, port))
		except socket.error as e:
			print(str(e))

		
		
		self.num_threads = 0
		self.max_threads = 1
		self.clients = []

		s.listen(5)

		print('waitin for connection')


	def begin_server(self):
		while True:
			conn, addr = self.s.accept()
			
			if self.max_threads > self.num_threads:
				self.clients.append(conn)
				print('connected to client' + str(conn))
				start_new_thread(threaded_client_handler,(self, conn))
			else:
				start_new_thread(threaded_exit_handler, (self, conn))

	def sendToAll(self, data, sourceClient):
		for conn in self.clients:
			if conn != sourceClient:
				conn.send(data.encode('utf-8'))

	


if __name__ == "__main__":
	server().begin_server()
