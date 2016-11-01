import ftplib

def anonLogin(hostname):

	try:
		ftp = ftplib.FTP(hostname)
		ftp.login('anonymous', 'me@you.com')
		print '\n[*] ' +str(hostname) +\
			' FTP Anonymous Logon succeed.'
		ftp.quit()
		return True

	except Exception, e:
		print '\n[-] ' + str(hostname) +\
			' FTP Anonymous Logon Failed.'
		return False

host = '192.168.95.179'
anonLogin(host)


