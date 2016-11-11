from scapy.all import *
from bluetooth import *

def retBtAddr(addr):

	btAddr = str(hex(int(addr.replace(':', ''), 16) + 1))[2:]
	btAddr = btAddr[0:2]+":"+btAddr[2:4]+":"+btAddr[4:6]+":"+\
	return btAddr

def checkBluetooth(btAddr):

	btName = lookup_name(btAddr)

	if btName:
		print '[+] Detected Bluetooth Device: ' + btName
	else:
		print '[-] Failed to Detect Bluetooth Device.'

def wifiPrint(pkt):

	iPhone_OUI = 'd0:23:db'

	if pkt.haslayer(Dotll):
		wifiMac = pkt.getlayer(Dotll).addr2

		if iPhone_OUI == wifiMac[:8]:
			print '[*] Detected iPhone MAC: ' + wifiMac
			btAddr = retBtAddr(wifiMac)
			print '[+] Testing Bluetooth MAC: ' + btAddr

			checkBluetooth(btAddr)
			conf.iface = 'mon0'
			sniff(prn=wifiPrint)



