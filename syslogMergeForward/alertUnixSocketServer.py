#!/bin/env python
#coding=utf-8
import ConfigParser
import threading,os,sys
import logging as logObj
import hashlib,copy
#timer lib
from mylib import myTimer as myTimer

#common function lib
from mylib import common
#socket daemon main 
from mylib import transactionFrame
#global variable and queue declare, timer reset func
from inc import include as globalVariable
#dispatcher main msg thread
from plugin import dispatcherQueueNode as dispatcherQueueNode
#dispatcher filterMsg thread
from plugin import dispatcherMsgFilterQueueNode as dispatcherMsgFilterQueueNode
#send email thread
from plugin import processEmailQueue as processEmailQueue
#send sms thread
from plugin import processSMSQueue as processSMSQueue

#send sendmail thread
#from plugin import processSendmailQueue as processSendmailQueue

#send msgFilter sendmail thread
from plugin import processFilterMsgEmailQueue as processFilterMsgEmailQueue

#syslogNodeData = { 'msgID': { 'title':'title', 'body':'body','level':'warning', 'msgCount':0 } }
#init email queue



def help( argv ):
    if len( sys.argv ) != 2:
        print "start error: python alertUnixSocketServer.py unixSocketDaemon.ini"
        exit
    return

help( sys.argv )


#init configure 
cf = ConfigParser.ConfigParser()
cf.read( sys.argv[1] )
conf = common.convertListToDict( cf )

tmpVal = conf['processPolicy']['enablestatus']
conf['processPolicy']['enablestatus'] = tuple(tmpVal.split(','))
tmpVal = conf['processPolicy']['enableservername']
conf['processPolicy']['enableservername'] = tuple(tmpVal.split(','))


tmpVal = conf['msgFilter']['item1'].split('|')
conf['msgFilter'] = dict()
retArr=dict()
conf['msgFilterMail']['mergeflag'] = int(conf['msgFilterMail']['mergeflag'])

for i in range(len(tmpVal)):
    tmpVal2 = tmpVal[i].split(':')
    print tmpVal2
    retArr['maxCount'] = int(tmpVal2[3])
    retArr['serviceName'] = tmpVal2[0]
    retArr['moduleName'] = tmpVal2[1]
    tmpVal3 = tmpVal2[2].split(',')
    retArr['filterStr'] = tmpVal3
    print tmpVal3
    tmpStr=''
    for j in range(len(retArr['filterStr'])):
        tmpStr = tmpStr+retArr['filterStr'][j]
    id = hashlib.new("md5",tmpStr).hexdigest()
    tmpVal4 = tmpVal2[4].split(',')
    retArr['toMailList'] = tmpVal4
    retArr['sendType'] = int(tmpVal2[5])
    #notice需要使用copy否则原值无效
    conf['msgFilter'][id]=copy.copy(retArr)
 
#format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
#init log obj
logObj.basicConfig(filename=conf[ 'log' ][ 'access' ],filemode='a+',level=logObj.INFO, format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s %(filename)s %(module)s %(lineno)d', datefmt='%Y-%m-%d %H:%M:%S' )

#build email object

#start timer set for rsyslog push merge log to center 
myTimer1 = myTimer.myTimer( int( conf[ 'queue' ][ 'mergelogperiod' ] ), logObj, 'rsyslog' )
myTimer1.start()


#start timer set for alert msg  period
myTimer2 = myTimer.myTimer( int( conf[ 'queue' ][ 'alertmsgperiod' ] ), logObj, 'nginx' )
myTimer2.start()

#start timer set for msgFilter push merge log to msgFilterData 
myTimer3= myTimer.myTimer( int( conf[ 'queue' ][ 'mergelogperiod' ] ), logObj, 'msgFilter' )
myTimer3.start()

#dispatcher reciveQueue node to email and sms queue
dispatcherQueueNodeObj = dispatcherQueueNode.dispatcherQueueNode( conf, logObj )
dispatcherQueueNodeObj.start()

#dispatcher msgFilter reciveQueue node to msgFilterData queue
dispatcherMsgFilterQueueNodeObj = dispatcherMsgFilterQueueNode.dispatcherMsgFilterQueueNode( conf, logObj )
dispatcherMsgFilterQueueNodeObj.start()


#block emailQueue and sendmail this is single thread
processEmailQueueObj = processEmailQueue.processEmailQueue( conf, logObj )
processEmailQueueObj.start()

#block msgFilterData and sendmail this is single thread
processFilterMsgEmailQueueObj = processFilterMsgEmailQueue.processFilterMsgEmailQueue( conf, logObj )
processFilterMsgEmailQueueObj.start()

#block smsQueue this is single thread(system curl send sms)
processSMSQueueObj = processSMSQueue.processSMSQueue( conf, logObj )
processSMSQueueObj.start()


#block sendmail this is single thread
#processSendmailQueue = processSendmailQueue.processSendmailQueue( conf, logObj )
#processSendmailQueue.start()

#build transaction frame object
server = transactionFrame.transactionFrame( conf, logObj )

#print conf
try:
    transactionFrame.asyncore.loop()

finally:
    if os.path.exists( conf[ 'socketInfo' ][ 'socket' ] ):
        os.unlink( conf[ 'socketInfo' ][ 'socket' ] )
