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
		# after talking about it, a fix that should be added is checking for length of message 
		# and ensuring the whole message is received before trying to do anything with that message
		data = conn.recv(2048).decode('utf-8')
		if not data:
				break

		server.handleClientData(data, conn)
	server.num_threads -= 1
	print('client disconnect, total number remaining: ' + str(server.num_threads))
	
	for c in server.clients:
		if c == conn:
			server.clients.remove(c)
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

		# allow max_threads to be easy to change
		self.max_threads = 3
		
		# list of clients connected
		self.clients = []
		self.loggedInClients = []
		self.client_user_list = []

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

		if command[0] == 'help':
			client.send(str('Commands: Login <username>\nsend').encode('utf-8'))
		elif command[0] == 'login':
			if len(command) == 2:
				username, password = command[1].split(' ', 1)
				for user in self.users:
					if username.lower() == user['username'].lower():
						if password == user['password']:
							for conn in self.clients:
								if conn == client:
									
									''' 
										if I was going to be truly OO design conscious, I would make a class for this list so that I could
										build out logging in and all that, but honestly this stuff should be persisted in a database
										anyway so whatever
									'''

									self.loggedInClients.append(conn)
									self.client_user_list.append([conn, username])
									
									client.send(str('Welcome ' + user['username']).encode('utf-8'))
									self.sendToAll(str(user['username'] + ' joined the room'), client)
						else:
							client.send(str('login incorrect').encode('utf-8'))
		elif client in self.loggedInClients:
			if command[0] == 'send':
				if len(command) > 1:
					recipient, msg = command[1].split(' ', 1)
					
					if recipient.lower() == 'all':

						for item in self.client_user_list:
							if client == item[0]:
								user = item[1]

								self.sendToAll(str(user + '>> ' + msg), client)
					else:
						for item in self.client_user_list:
							if recipient.lower() == item[1]:
								item[0].send(str(item[1] + "(direct message)>> " + msg).encode('utf-8'))
							else:
								client.send(str('The user requested for messaging is not logged in or does not exist').ecnode('utf-8'))

			# if send UserID
			''' send message to server, let server send to userID matched by name '''
			# who 
			''' list who is in the room '''

			# logout
			''' close connection and leave. others notified of leaving '''

		else:
			client.send(str('You must login before you may access this chat service').encode('utf-8'))
	


if __name__ == "__main__":
	server().begin_server()
