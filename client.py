import os
import socket
import sys
import select

class connRefusedExcept(Exception):
	'''raise this when connection is refused'''


class ChatClient(object):
	def __init__(self, host, port):
		self.flag = False
		self.port = int(port)
		self.host = host

		# Attempt to connect to server at port 

	def start(self):
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect((self.host, self.port))
			print('Connected to chat server %s:%d' % (self.host, self.port))
		except Exception as e:
			print('Exception %s' % str(e))
		while not self.flag:
			# do stuff
			try:
				sys.stdout.write('')
				sys.stdout.flush()
				inputready, outputready, exceptrdy = select.select([0, self.sock], [], [])

				for i in inputready:
					print(str(i))
					if i == 0:
						data = sys.stdin.readline().strip()

						if data:
							self.sock.send(data.encode('utf-8'))
					elif i == self.sock:
						data = self.sock.recv(2048).decode('utf-8')
						if data == str('close_client'):
							input('press enter to cont, received close')
							self.flag = True
							raise connRefusedExcept('conn closed')

						sys.stdout.write(data + '\n')
						sys.stdout.flush()
					else:
						print(str(i))
						print('This is the self.sock' + str(self.sock))
			except connRefusedExcept as e:
				print(str(e))
			except Exception as e:
				print('Exception occurred:' + str(e)) 	
				self.sock.close()
		self.sock.close()
		sys.exit()

if __name__ == "__main__":
	if len(sys.argv) < 3:
		sys.exit('Usage: %s listen_ip listen_port' % sys.argv[0])

	ChatClient(sys.argv[1], sys.argv[2]).start()
