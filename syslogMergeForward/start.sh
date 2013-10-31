#!/bin/sh
ps ax|grep alertUnixSocketServer|grep -v "grep"|grep -v "log"|awk '{print "kill -9 "$1}'|sh;rm -f /tmp/alertDaemon.sock;python ./alertUnixSocketServer.py  ./conf/mergeLog.ini 2>/tmp/alertUnixServer.err.log 1>/tmp/alertUnixServer.acc.log&

