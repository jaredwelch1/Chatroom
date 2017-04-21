import socket
import sys
from _thread import *
import json


def threaded_client_handler(conn):
	conn.send(str.encode('Welcome, these commands are available: '))

	while True:
		data = conn.recv(2048)
		if not data:
				break
		print("received: " + data.decode('utf-8'))
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

		s.listen(5)
		print('waitin for connection')


	def begin_server(self):
		while True:

			conn, addr = self.s.accept()
			print('connected to client')
			start_new_thread(threaded_client_handler,(conn,))



if __name__ == "__main__":
	server().begin_server()
