
import socket
import srv.config
import threading

class Listener:
	def __init__(self,listenaddress,callback):
		"""
			sets up a socket in the given address (host,port)
			callback will be called for each incoming connection
		"""
		self.sock = socket.socket()
		self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		self.sock.bind(listenaddress)
		self.sock.listen(srv.config.listenbacklog)
		self.callback=callback

	def loop(self):
		self.running=True
		self.t = threading.Thread(target=self._loop)
		self.t.start()

	def _loop(self):
		while self.running:
			try:
				data,address = self.sock.accept()
			except:
				if self.running:
					raise
			else:
				self.callback(data,address)

	def shutdown(self):
		if self.running:
			self.running=False
			self.sock.shutdown(socket.SHUT_RDWR)
			self.t.join()

