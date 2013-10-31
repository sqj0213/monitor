#!/bin/env python
#coding=utf-8
import threading
import hashlib,copy
import syslog
from inc import include as globalVariable

class dispatcherMsgFilterQueueNode( threading.Thread ):
    def __init__( self, conf, _logObj ):
        self.logObj = _logObj
        self.conf = conf
        self.stopFlag = False
        threading.Thread.__init__( self )
    def stop( self ):
        self.stopFlag = True


    def mergeLog( self, nodeData ):
	#如果sendtype为0的话则按模板发送，否则直接发送日志内容
	if ( type(nodeData) == type(list())):
                nodeDataKey = nodeData[0]
                nodeDataValue = nodeData[1]
	else:
		nodeDataKey = nodeData
        if ( globalVariable.msgFilterData.has_key(nodeDataKey) ):
        	globalVariable.msgFilterData[nodeDataKey]['count'] = globalVariable.msgFilterData[nodeDataKey]['count'] + 1
        else:
		globalVariable.msgFilterData[nodeDataKey] = {}
       		globalVariable.msgFilterData[nodeDataKey]['count'] = 1
		if ( type(nodeData) == type(list())):
        		globalVariable.msgFilterData[nodeDataKey]['value'] = nodeDataValue
        if globalVariable.msgFilterData[nodeDataKey]['count'] >= self.conf['msgFilter'][nodeDataKey]['maxCount']:
       		globalVariable.msgFilterAlertFlag = True
        self.logObj.info('mergeLog complete!'+str(globalVariable.msgFilterData[nodeDataKey]['count'])+':'+str(self.conf['msgFilter'][nodeDataKey]['maxCount']))
    #rewrite thread main
    def run( self ):
        #global globalVariable.totalEmailCount,globalVariable.syslogEmailNodeData,globalVariable.mutexEmail
        #notice queue is null , block
        self.logObj.info( "dispatcherMsgFilterQueueNode thread is start!" )
        while True:
            if self.stopFlag:
                self.logObj.info( "dispatcherMsgFilterQueueNode thread is shutdown!" )
                break
            queueNode = globalVariable.msgFilterReciveQueue.get()

            self.mergeLog(queueNode)
            #hostname_uri_200
            #若报警标志为需要报警则把要报警信息推入报警队列
            if globalVariable.msgFilterAlertFlag:
                self.logObj.info('recive msgFilter up maxCount and build mail datastruct begin!')
		pushList=[]
                tmpVal={}
                for k in globalVariable.msgFilterData:
                    alertCount = globalVariable.msgFilterData[k]['count']
		    #notice dict give value and reset dict
                    tmpVal = self.conf['msgFilter'][k]
		    #若启用合并发送则赋值mailtitle的key
		    if ( self.conf['msgFilterMail']['mergeflag'] == 1 ):
                	self.logObj.info('debug('+str(alertCount)+":"+str(self.conf['msgFilter'][k]['maxCount'])+")")
		    	if ( alertCount >= self.conf['msgFilter'][k]['maxCount'] ):
				tmpVal['alertKey'] = k
                    tmpVal['alertCount'] = alertCount
		    #若发送邮件类型为直接发送日志内容的话，进行日志内容的赋值
		    if ( tmpVal['sendType'] == 1 ):
			tmpVal['sendContent'] =  globalVariable.msgFilterData[k]['value']
		    #若启用合并发送则先合并
		    if ( self.conf['msgFilterMail']['mergeflag'] == 1 ):
		    	pushList.append(tmpVal)
		    #否则入队列进行发送
		    else:
                	globalVariable.msgFilterMailQueue.put(copy.deepcopy(tmpVal))
		#若合并发送则入队列
		if ( self.conf['msgFilterMail']['mergeflag'] == 1 ):
                	globalVariable.msgFilterMailQueue.put(copy.deepcopy(pushList))
                globalVariable.msgFilterData={}
                globalVariable.msgFilterAlertFlag=False
                self.logObj.info('recive msgFilter up maxCount and build mail datastruct end!')
            #若报警定时器为到时状态，则重置报警消息,重新计数
            if globalVariable.timeSendMsgFilterFlag:
                self.logObj.info('send msgFilter period is true and reset send msgFilter period flag begin(msgFilter)!')
                globalVariable.msgFilterData={}
                globalVariable.msgFilterAlertFlag=False
                globalVariable.timeSendMsgFilterFlag = False
                self.logObj.info('send msgFilter period is true and reset send msgFilter period flag end(msgFilter)!')

