import ConfigParser
import socket
import sys, types

from mylib import common
from plugin import processEmailQueue as processEmailQueue



cf = ConfigParser.ConfigParser()
cf.read( "conf/unixSocketDaemon.ini" )



confDict = common.convertListToDict( cf )






# Create a UDS socket
sock = socket.socket( socket.AF_UNIX, socket.SOCK_DGRAM )

# Connect the socket to the port where the server is listening
server_address = confDict['socketInfo' ][ 'socket' ]
print >>sys.stderr, 'connecting to %s' % server_address
try:
    sock.connect( server_address )
    # Send data
    message1 = "3|test email|msg body"
    message2 = "4|error| msg body"
    sock.send( message1 )
    sock.send( message2 )


finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
