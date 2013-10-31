#!/bin/env python
#coding=utf-8
import ConfigParser
import socket
import sys, types

from mylib import common
from plugin import processEmailQueue as processEmailQueue



cf = ConfigParser.ConfigParser()
cf.read( "conf/mergeLog.ini" )



confDict = common.convertListToDict( cf )


# Create a UDS socket
sock = socket.socket( socket.AF_UNIX, socket.SOCK_DGRAM )

# Connect the socket to the port where the server is listening
server_address = confDict['socketInfo' ][ 'socket' ]
print >>sys.stderr, 'connecting to %s' % server_address
try:
    sock.connect( server_address )
    # Send data
    message1 = "013-03-11 14:13:35 INFO  [root] <190>Mar 11 14:13:35 cancer-hz5 webFront-nginx-z-access: z.gexing.com  2013-03-11T14:09:07+08:00  GET /api/index.php?callback=jQuery172004668953955008265_1362982159968&action=ajax_getLoginStatus&_=1362982168937 HTTP/1.1  /api/index.php  http://www.gexing.com/zt/qqtouxiang/513.html  118.254.168.101  126  rc:200  Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 718)  0.003"
    message2 = "013-03-11 14:13:35 INFO  [root] <190>Mar 11 14:13:35 cancer-hz5 webFront-nginx-z-access: z.gexing.com  2013-03-11T14:09:07+08:00  GET /api/index.php?callback=jQuery172004668953955008265_1362982159968&action=ajax_getLoginStatus&_=1362982168937 HTTP/1.1  /api/index.php  http://www.gexing.com/zt/qqtouxiang/513.html  118.254.168.101  126  rc:500  Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 718)  0.003"
    message3 = "013-03-11 14:13:35 INFO  [root] <190>Mar 11 14:13:35 cancer-hz5 webFront-nginx-z-access: z.gexing.com  2013-03-11T14:09:07+08:00  GET /api/index.php?callback=jQuery172004668953955008265_1362982159968&action=ajax_getLoginStatus&_=1362982168937 HTTP/1.1  /api/index.php  http://www.gexing.com/zt/qqtouxiang/513.html  118.254.168.101  126  rc:502  Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 718)  0.003"
    message4 = "013-03-11 14:13:35 INFO  [root] <190>Mar 11 14:13:35 cancer-hz5 mysql-messages:  kernel: "
#    sock.send( message1 )
#    sock.send( message2 )
#    sock.send( message3 )
    sock.send( message4 )

    message1 = "013-03-11 14:13:35 INFO  [root] <190>Mar 11 14:13:35 cancer-hz5 webFront-nginx-www-access: www.gexing.com  2013-03-11T14:09:07+08:00  GET /api/index.php?callback=jQuery172004668953955008265_1362982159968&action=ajax_getLoginStatus&_=1362982168937 HTTP/1.1  /api/index.php  http://www.gexing.com/zt/qqtouxiang/513.html  118.254.168.101  126  rc:200  Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 718)  0.003"
    message2 = "013-03-11 14:13:35 INFO  [root] <190>Mar 11 14:13:35 cancer-hz5 webFront-nginx-www-access: www.gexing.com  2013-03-11T14:09:07+08:00  GET /api/index.php?callback=jQuery172004668953955008265_1362982159968&action=ajax_getLoginStatus&_=1362982168937 HTTP/1.1  /api/index.php  http://www.gexing.com/zt/qqtouxiang/513.html  118.254.168.101  126  rc:500  Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 718)  0.003"
    message3 = "013-03-11 14:13:35 INFO  [root] <190>Mar 11 14:13:35 cancer-hz5 webFront-nginx-www-access: www.gexing.com  2013-03-11T14:09:07+08:00  GET /api/index.php?callback=jQuery172004668953955008265_1362982159968&action=ajax_getLoginStatus&_=1362982168937 HTTP/1.1  /api/index.php  http://www.gexing.com/zt/qqtouxiang/513.html  118.254.168.101  126  rc:502  Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 718)  0.003"
    message4 = "013-03-11 14:13:35 INFO  [root] <190>Mar 11 14:13:35 cancer-hz5 pic.upload-server:  kernel: fatal"
#    sock.send( message1 )
#    sock.send( message2 )
#    sock.send( message3 )
    sock.send( message4 )


finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
