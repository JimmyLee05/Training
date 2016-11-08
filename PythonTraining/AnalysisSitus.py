import pygeoip

gi = pygeopy.GeoIP('/opt/GeoIP/Geo.dat')

def prientRecord(tgt):

	rec = gi.record_by_name(tgt)
	city = rec['city']
	region = rec['region_name']
	country = rec['country_name']
	long = rec['longitude']
	lat = rec['latitude']
	print '[*] Target: ' + tgt + 'Geo-located'
	print '[+] '+str(city)+', '+str(region)+', '+str(country)
	print '[+] Latitude: '+str(lat)+ ', Longitude: '+ str(long)

tgt = '173.255.226.98'
prientRecord(tgt)

