#!/bin/env python
#coding=utf-8
import threading
import copy,time,commands
from inc import include as globalVariable

class processSMSQueue(  threading.Thread ):

    toMobileList = []
    msgTmpl = ""
    smsUrl = ""
    conf = {}

    def __init__( self, conf, _logObj ):
        self.logObj = _logObj
        self.conf = conf
        self.stopFlag = False
        self.reloadFlag = False
        self.toMobileList = self.conf[ 'sms' ][ 'mobile' ]
        self.msgTmpl = self.conf[ 'sms' ][ 'msgtmpl' ]
        self.smsUrl = self.conf[ 'sms' ][ 'smsurl' ]
        threading.Thread.__init__( self ) 


    def buildSMSBody( self, msgNode ):
        #时间:__TIME__,主机名:__SERVERNAME__,错误次数:__REQUESTCNT__,状态码:__STATUS__
        smsMsg = ''
        tmpBodyStr = self.msgTmpl
        statusList = self.conf['processPolicy']['enablestatus']
        serverNameList = self.conf['processPolicy']['enableservername']
        for tmp in range( len( statusList ) ):
            status = int(statusList[tmp])
            if ( status != 200 and status !=304 ):

                for tmp1 in range(len( serverNameList)):
                    domain = serverNameList[tmp1]
                    if ( msgNode.has_key(domain) ):
                        if ( msgNode[domain].has_key(status)):
                            tmpBodyStr1 = tmpBodyStr.replace('__SERVERNAME__', domain )
                            tmpBodyStr1 = tmpBodyStr1.replace('__REQUESTCOUNT__', str(msgNode[domain][status]['requestCount']) )
                            tmpBodyStr1 = tmpBodyStr1.replace('__STATUS__', str(status) )
                            smsMsg =  smsMsg +"|" + tmpBodyStr1
        globalVariable.totalSMSCount += 1
        return "时间:"+ str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))) + smsMsg
    def stop( self ):
        self.stopFlag = True
    def reload( self ):
        self.reloadFlag = True

    def writeLog( self, summary, detail ):
        
        return

    def sendSMS( self, msgDetail ):
        smsMSG = self.buildSMSBody( msgDetail )
        cmdStr = self.smsUrl.replace( '__MSG__', smsMSG );
        cmdStr = cmdStr.replace( '__MOBILE__', self.toMobileList );
        retMsg = commands.getoutput( "/usr/bin/curl \""+cmdStr+"\"" )
        logStr = "send sms info(cmdStr("+cmdStr+")retMsg("+retMsg+"))"
        self.logObj.info( logStr )
    def run( self ):
        self.logObj.info( "send sms thread start!" )
        while ( True ):
            if self.stopFlag:
                self.logObj.info( "thread is shutdown" )
                break
            #if self.reload:
            #   pass
            #notice this cmd will block 
            emailSMSNode = globalVariable.smsQueue.get()
            #notice copy no pointer
            print emailSMSNode
            self.logObj.info("send sms begin!")
            self.sendSMS( emailSMSNode )
            self.logObj.info("send sms end!")

            #notice this must be clear for mem
            globalVariable.smsQueue.task_done()
            emailSMSNode.clear()
