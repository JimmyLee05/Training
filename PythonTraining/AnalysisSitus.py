import dpkt
import socket
import pygeoip
import optparse

gi = pygeoip.GeoIP('/opt/GeoIP/Geo.dat')

def retGeoStr(ip):

	try:
		rec = gi.record_by_name(ip)
		city = rec['city']
		country = rec['country_code3']

		if city != '':
			geoLoc = city +', ' +country

		else:
			geoLoc = country

		return geoLoc

	except Exception, e:
		return 'unregistered'

def printPcap(pcap):

	for (ts, buf) in pcap:
		try:
			eth = dpkt.ethernet.Ethernet(buf)
			ip = eth.data
			src = socket.inet_ntoa(ip.src)
			dst = socket.inet_ntoa(ip.dst)
			print '[+] Src: ' +src +' --> Dst: ' +dst
			print '[+] Src: ' +retGeoStr(src) +' --> Dst: ' \
				+retGeoStr(dest)
		except:
			pass

def main():

	parser = optparse.OptionParser('usage%prog -p <pcap file>')
	parser.add_option('-p', dest='pacpFile', type='string',\
		help='specify pcap filename')
	(options, args) = parser.parse_args()

	if options.pcapFile == None:
		print parser.usage
		exit(0)
	pcapFile = options.pacpFile
	f = open(pcapFile)
	pacp = dpkt.pcap.Reader(f)
	printPcap(pcap)

if __name__ == '__main__':
	main()

	
