#!/bin/env python
#coding=utf-8
import threading, time
from inc import include as globalVariable
class myTimer( threading.Thread ):
    def __init__( self, interval, logObj, module='nginx' ):
        threading.Thread.__init__( self )
        self.logObj = logObj
        self.stopFlag = False
        self.interval = interval
        self.module = module
    def stop( self ):
        self.stopFlag = True
    def run( self ):
        while True:
            if self.stopFlag:
                break
            #取得5分钟的整数时间
	    if self.module == 'rsyslog':
            	globalVariable.currentTime = int(time.time())/self.interval*self.interval
            	globalVariable.lastAlertTime= int(time.time())
            	self.logObj.info( "timer is set timeWriteRsyslogFlag true" )
            	globalVariable.timeWriteRsyslogFlag = True
            	time.sleep( self.interval )
	    if self.module == 'nginx':
            	globalVariable.lastAlertTime= int(time.time())
            	self.logObj.info( "timer is set timeSendMsgFlag true" )
            	globalVariable.timeSendMsgFlag = True
            	time.sleep( self.interval )
	    if self.module == 'msgFilter':
            	globalVariable.lastFilterAlertTime= int(time.time())
                self.logObj.info( "timer is set timeSendMsgFilterFlag true" )
                globalVariable.timeSendMsgFilterFlag = True
                time.sleep( self.interval )
