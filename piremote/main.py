import logging
import argparse #parser for cmd line options, args and sub-commands
import os
import sys
import netifaces
import tornado.ioloop
from tornado.log import access_log, app_log
from piremote import control
from piremote.application import application

if sys.version_info < (3,):
	ustr = unicode
else:
	ustr = str

parser = argparse.ArgumentParser(description= 
		'Presentation remote controller server')
parser.add_argument('-a', '--address', type = str, default = '0.0.0.0', help = 'Listening address')
parser.add_argument('-p', '--port', type = int, default = 1234, help = 'Listening TCP port')
parser.add_argument('-k', '--key', type = ustr, default = '', help = 'Password')

def print_info(address, port):
	ifaces = netifaces.interfaces()
	if address != "0.0.0.0":
		ips = [address]
	else:
		ips = []
		for iface in ifaces:
			addresses = netifaces.ifaddresses(iface).get(netifaces.AF_INET, [])
			# collect every interface address except localhost
			for addrinfo in addresses:
				ip = addrinfo['addr']
				if ip == "127.0.0.1":
					continue
				ips.append(ip)
				
	if len(ips) > 0:

		print("Navigate to one of these addresses on your phone's browser to run the remote " +
			"control interface.\n")
		for ip in ips:
			print("http://%s:%d/\n" % (ip, port))



def main():
	# use line buffer
	sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1)
	sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', 1)
	args = parser.parse_args()
	key = args.key

	if key is None:
		print("A key is needed: use -k option to provide it")
		sys.exit(1)
	
	# it's the key set by the user
	control.app_key = key

	# set logging level 
	access_log.setLevel(logging.INFO)

	# specifies to tornado app on which address:port it has to listen to
	application.listen(args.port, address = args.address)

	tornado.ioloop.IOLoop.instance().add_timeout(0, lambda: print_info(args.address, args.port))

	try:
		tornado.ioloop.IOLoop.instance().start()
	except KeyboardInterrupt:
		pass

if __name__ == "__main__":
	main()