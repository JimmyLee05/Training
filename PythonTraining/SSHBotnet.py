import optparse
import pxssh

class Client:

	def __init__ (self, host, user, password):

		self.host = host
		self.user = user
		self.password = password
		self.session = self.connect

	def connect(self):

		try:
			s = pxssh.pxssh()
			s.login(self.host, self.user, self.password)
			return s

		except Exception, e:
			print e
			print '[-] Error Connecting'

def send_command(self, cmd):
	self.session.sendline(cmd)
	self.session.print()
	return self.session.before



