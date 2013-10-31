#!/bin/env python
#coding=utf-8
import threading
import Queue

protocalDataColumnCount=11
protocalStatusColumn=8
protocalServerNameColumn=1
protocalHostNameColumn=0
protocalUriColumn=4
#gexing-access  cancer-hz5   www.gexing.com  2013-02-03T22:59:54+08:00
# GET /api/index.php?callback=jQuery17203404815510426171_1359844346563&action=ajax_getLoginStatus&_=1359844347031 HTTP/1.1  /api/index.php
# http://www.gexing.com/u/7180228/fs/6  182.234.64.129  122  200  Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; InfoPath.1)  0.004
"""
CREATE TABLE `nginx-200-interval5m` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostName` char(20) DEFAULT NULL,
  `serverName` char(100) DEFAULT NULL,
  `uri` char(255) DEFAULT NULL,
  `httpBodySize` int(11) DEFAULT NULL,
  `httpStatus` int(11) DEFAULT NULL,
  `httpRequestTime` int(11) DEFAULT NULL,
  `timeInterval` datetime NOT NULL,
  `regTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8$$
"""
protocalDataTmpl = {'serverName':'','hostName':'','uri':'','requestCount':0, 'httpBodySize':0, 'httpStatus':200,'httpRequestTime':0,'timeInterval':0}
protocalData = {}
alertData = {}
lastAlertTime=0

msgFilterDataTmpl = {'xxxxxx':['pic-upload','fatal'],'maxCount':3,'toMailList':['sunquanjun@gexing.com','sqj0213@163.com']}
msgFilterData = {}
msgFilterMailData={}
msgFilterAlertFlag = False
lastFilterAlertTime=0

totalEmailCount = 0
totalSMSCount = 0
totalMsgFilterEmailCount=0


#当前时间周期
currentTime=0

#DECLARE email sms lock
#global mutexEmail,mutexSMS
#init sms email lock
#recive msg queue
reciveQueue = Queue.Queue()
emailQueue = Queue.Queue()
smsQueue = Queue.Queue()
msgFilterReciveQueue = Queue.Queue()
msgFilterMailQueue=Queue.Queue()
sendmailQueue = Queue.Queue()
nginx200LogQueue = Queue.Queue()
nginxNot200LogQueue = Queue.Queue()

#timer flag for save to actionQueue
timeSendMsgFlag = False


def setSendMsgTimeFlag( _logObj ):

    _logObj.info( "send msg timer is set timeSendMsgFlag true" )
    timeSendMsgFlag = True


#msgFilter flag for reset msgFilterData queue
timeSendMsgFilterFlag = False

def setSendMsgFilterTimeFlag( _logObj ):

    _logObj.info( "send msgFilter timer is set timeSendMsgFilterFlag true" )
    timeSendMsgFilterFlag = True

#timer flag for save to actionQueue
timeWriteRsyslogFlag = False

def setWriteRsyslogTimeFlag( _logObj ):

    _logObj.info( "write rsyslog is set timeWriteRsyslogFlag true" )
    timeWriteRsyslogFlag = True
