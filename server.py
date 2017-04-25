import socket
import sys
from _thread import *
import json

def threaded_exit_handler(self, conn):
	#conn.send(str.encode('close_client'))
	conn.close()
	

def threaded_client_handler(server, conn):
	server.num_threads += 1
	print('connected to client, count of total clients = ' + str(server.num_threads))
	conn.send(str.encode('Welcome, please log in using <login> <user> <pass>'))


	while True:
		data = conn.recv(2048).decode('utf-8')
		if not data:
				break

		server.handleClientData(data, conn)
	server.num_threads -= 1
	print('client disconnect, total number remaining: ' + str(server.num_threads))
	conn.close()


class server(object):

	def __init__(self, host='127.0.0.1', port=15109):

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
				start_new_thread(threaded_client_handler,(self, conn))
			else:
				start_new_thread(threaded_exit_handler, (self, conn))

	def sendToAll(self, data, sourceClient):
		for conn in self.clients:
			if conn != sourceClient:
				conn.send(data.encode('utf-8'))

	def handleClientData(self, data, client):
		command = data.split(' ', 1)
		print(str(self.clients))
		if command[0] == 'help':
			client.send(str('Commands: Login <username>\nsend').encode('utf-8'))
		else:
			client.send(str('The command you gave is unknown or formatted incorrectly. Type help to see commands').encode('utf-8'))
	


if __name__ == "__main__":
	server().begin_server()
