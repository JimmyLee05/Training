import zipfile

zFile = zipfile.ZipFile('evil.zip')
passFile = open('dictionary.txt')

for line in passFile.readlines():

	password = line.strip('\n')

	try:

		zFile.extractall(pwd=password)
		print '[+] Password = ' +password + '\n'
		exit(0)

	except Exception, e:
		pass
