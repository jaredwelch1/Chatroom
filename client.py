import os
import socket
import sys
import select


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
			print('Connected to chat esrver %s:%d' % (self.host, self.port))
		except Exception as e:
			print('Exception %s' % str(e))
		while not self.flag:
			# do stuff
			try:
				sys.stdout.write('')
				sys.stdout.flush()
				inputready, outputready, exceptrdy = select.select([0, self.sock], [], [])

				for i in inputready:
					if i == 0:
						data = sys.stdin.readline().strip()

						if data:
							self.sock.send(data.encode('utf-8'))
			except Exception as e:
				print('Exception occurred:' + str(e))
				close()
		self.sock.connect.close()

if __name__ == "__main__":
	if len(sys.argv) < 3:
		sys.exit('Usage: %s listen_ip listen_port' % sys.argv[0])

	ChatClient(sys.argv[1], sys.argv[2]).start()
