"""
	Connection handling
"""

import socket

class Connection:
	def Login(self):
		s = socket.create_connection(["127.0.0.1",6666])
		self.conn=s.makefile()
		return self.conn

