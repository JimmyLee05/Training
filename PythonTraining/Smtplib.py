import smtplib
from email.mime.text import MIMEtext

def sendMail(user,pwd,to,subject,text):

	msg = MIMeText(text)
	msg['FROM'] = user
	msg['TO'] = to
	msg['Subject'] = subject

	try:
		smtpServer = smtplib.SMTP('smtp.gmail.com', 587)
		print "[+] Connecting To Mail Server."
		smtpServer.ehlo()
		print "[+] Starting Encrypted Session."
		smtpServer.starttls()
		smtpServer.ehlo()
		print "[+] Logging Into Mail Server."
		smtpServer.login(user, pwd)
		print "[+] Sending Mail."
		smtpServer.sendmail(user, to, msg.as_string())
		smtpServer.close()
		print "[+] Mail Sent Successfully."
	except:
		print "[-] Sending Mail Failed."

user = 'username'
pwd = 'password'
sendMail(user, pwd, 'target@tgt.tgt',\
	'Re: Important', 'Test Message')
