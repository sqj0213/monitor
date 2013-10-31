#!/bin/env python
#coding=utf8

import threading
from mylib import sendMail  as sendMail
import copy,time
from inc import include as globalVariable

class processFilterMsgEmailQueue( threading.Thread ):

    fromEmailInfo = { 'fromEmail':'', 'fromEmailPwd':'' }
    conf = {}

    def __init__( self, conf, _logObj ):
        self.logObj = _logObj
        self.conf = conf
        self.stopFlag = False
        self.fromEmailInfo[ 'fromEmail' ] = self.conf[ 'email' ][ 'fromemail' ]
        self.fromEmailInfo[ 'fromEmailPwd' ] = self.conf[ 'email' ][ 'fromemailpwd' ]
        threading.Thread.__init__( self )

    def stop( self ):
        self.stopFlag = True

    def sendMail( self, msgNode ):
        #alertData['500']['requestCount']=10
        #         ['www.gexing.com'][200]['requestCount']=5
        #
        """
print conf['msgFilter']
{'3c10c9e97fddae51e914ba17a787a57b': {'toMailList': ['sunquanjun@gexing.com', 'sqj0213@163.com'], 'serviceName': '"\xe5\xad\x98\xe5\x82\xa8', 'filterStr': ['pic.upload-server', 'fatal'], 'maxCount': '5'}, 
'50484c19f1afdaf3841a0d821ed393d2': {'toMailList': ['sunquanjun@gexing.com', 'sqj0213@163.com"'], 'serviceName': '\xe5\x85\xb6\xe5\xae\x83', 'filterStr': ['kernel'], 'maxCount': '3'}}

        """
        mailTitle = self.conf['msgFilterMail']['filtermailtmpl']
        mailBody = self.conf['msgFilterMail']['filtermailbody']
        toMailList = msgNode['toMailList']
        moduleName = msgNode['serviceName']
        mailTitle = mailTitle.replace('_MODULE_',msgNode['serviceName'])
        mailTitle = mailTitle.replace('_CNT_',str(msgNode['alertCount']))
	mailTitle = mailTitle.replace('_MINUTE_',str(int(time.time())-globalVariable.lastFilterAlertTime))
        tmpStr = ''
        for i in range(len(msgNode['filterStr'])):
            if (tmpStr == ''):
                tmpStr = msgNode['filterStr'][i]
            else:
                tmpStr = tmpStr+','+msgNode['filterStr'][i]
        dateTimeStr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()-2))
        mailTitle = mailTitle.replace('_STR_', tmpStr)

        mailBody = mailBody.replace( '_TIME_', dateTimeStr )
        mailBody = mailBody.replace( '_MODULE_', msgNode['moduleName'] )
        globalVariable.totalMsgFilterEmailCount += 1

        gexingServiceMailObj =  sendMail.gexingServiceMail( self.fromEmailInfo[ 'fromEmail' ] , self.fromEmailInfo[ 'fromEmailPwd' ] )
        gexingServiceMailObj.send( mailTitle, mailBody, toMailList )
        self.logObj.info( "send msgFilter email complete!to("+( '.'.join( toMailList ) )+")title("+mailTitle+")mailBody("+mailBody+")" )
    def sendMailByContent(self,msgNode):
	mailTitle = self.conf['msgFilterMail']['filtermailtmpl1']
        mailTitle = mailTitle.replace('_MODULE_',msgNode['serviceName'])
        mailTitle = mailTitle.replace('_CNT_',str(msgNode['alertCount']))
	mailTitle = mailTitle.replace('_MINUTE_',str(int(time.time())-globalVariable.lastFilterAlertTime))
        toMailList = msgNode['toMailList']
	mailBody = msgNode['sendContent']
        tmpStr = ''
        for i in range(len(msgNode['filterStr'])):
            if (tmpStr == ''):
                tmpStr = msgNode['filterStr'][i]
            else:
                tmpStr = tmpStr+','+msgNode['filterStr'][i]
        mailTitle = mailTitle.replace('_STR_', tmpStr)
        globalVariable.totalMsgFilterEmailCount += 1
        gexingServiceMailObj =  sendMail.gexingServiceMail( self.fromEmailInfo[ 'fromEmail' ] , self.fromEmailInfo[ 'fromEmailPwd' ] )
        gexingServiceMailObj.send( mailTitle, mailBody, toMailList )
        self.logObj.info( "send msgFilter email by Content complete!to("+( '.'.join( toMailList ) )+")title("+mailTitle+")mailBody("+mailBody+")" )
    def sendMergeMail(self,queueNode):
	toMailList = self.conf['msgFilterMail']['mergemaillist'].split(",")
	mailTitle,mailBody = self.buildMailTitleBody(queueNode)
        gexingServiceMailObj =  sendMail.gexingServiceMail( self.fromEmailInfo[ 'fromEmail' ] , self.fromEmailInfo[ 'fromEmailPwd' ] )
        gexingServiceMailObj.send( mailTitle, mailBody, toMailList )
        self.logObj.info( "send msgFilter merge email by Content complete!to("+( '.'.join( toMailList ) )+")title("+mailTitle+")mailBody("+mailBody+")" )
    def buildMailTitleBody(self,queueNode):
        self.logObj.info( "buildmailtitlebody begin!" )
	retMailBody = ""
	mailTitle = ""
	i = 1 
	dateTimeStr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()-2))
	intTime=int(time.time())
	for msgNode in queueNode:
		#邮件title处理
		if msgNode.has_key('alertKey'):
        		self.logObj.info( "buildmailtitlebody mailtitle begin!" )
			k = msgNode['alertKey']
			#是否启用发送模板
			if msgNode['sendType'] == 1:
				mailTitle = self.conf['msgFilterMail']['filtermailtmpl1']
			else:
				mailTitle = self.conf['msgFilterMail']['filtermailtmpl']
		        mailTitle = mailTitle.replace('_MODULE_',msgNode['serviceName'])
        		mailTitle = mailTitle.replace('_CNT_',str(msgNode['alertCount']))
        		mailTitle = mailTitle.replace('_MINUTE_',str(intTime-globalVariable.lastFilterAlertTime))
        		tmpStr = ''
        		for i in range(len(msgNode['filterStr'])):
            			if (tmpStr == ''):
                			tmpStr = msgNode['filterStr'][i]
            			else:
                			tmpStr = tmpStr+','+msgNode['filterStr'][i]
        		mailTitle = mailTitle.replace('_STR_', tmpStr)
        		self.logObj.info( "buildmailtitlebody mailtitle end!" )
		#邮件内容合并处理
        	self.logObj.info( "buildmailtitlebody sub mailbody begin num("+str(i)+")!")
		#filterMailBody=<a href="http://123.103.21.139:8080/hz/webFront/readLog.php?time=_TIME_&interval=150&domain=_MODULE_&idc=hz" target=_blank>详细日志</a>
		#filterMergeMailBodyTmpl=[_MODULE_]服务&nbsp;&nbsp;[_STR_]关键字&nbsp;&nbsp;[_MINUTE_]秒内&nbsp;&nbsp;[_CNT_]次&nbsp;&nbsp;内容:_CONTENT_
		mailBody = self.conf['msgFilterMail']['filtermergemailbodytmpl']	
		mailBody = mailBody.replace('_MODULE_',msgNode['serviceName'])
		mailBody = mailBody.replace('_CNT_',str(msgNode['alertCount']))
		mailBody = mailBody.replace('_MINUTE_',str(intTime-globalVariable.lastFilterAlertTime))
                tmpStr = ''
                for i in range(len(msgNode['filterStr'])):
                	if (tmpStr == ''):
                       		tmpStr = msgNode['filterStr'][i]
                        else:
                       		tmpStr = tmpStr+','+msgNode['filterStr'][i]
		mailBody = mailBody.replace( '_STR_', tmpStr )
		readLogUrl=self.conf['msgFilterMail']['filtermailbody']
		if ( msgNode['sendType'] == 0 ):
			readLogUrl=readLogUrl.replace('_MODULE_', msgNode['moduleName'])
			readLogUrl=readLogUrl.replace('_TIME_', dateTimeStr )
			mailBody = mailBody.replace('_CONTENT_', readLogUrl)
		else:
			mailBody = mailBody.replace('_CONTENT_',msgNode['sendContent'])
		if retMailBody == "":
			retMailBody = mailBody
		else:
			retMailBody = retMailBody+"<br><br>"+mailBody
        	self.logObj.info( "buildmailtitlebody sub mailbody end num("+str(i)+")!" )
		i = i + 1
	retMailBody = "时间:"+dateTimeStr+"<br><br>"+retMailBody
        self.logObj.info( "buildmailtitlebody end!" )
	return mailTitle,retMailBody
    def run( self ):
        self.logObj.info( "send msgFilter email thread start!" )
        while ( True ):
            if self.stopFlag:
                self.logObj.info( "send msgFilter email thread is shutdown!" )
                break
                #notice this cmd will block
            emailQueueNode = globalVariable.msgFilterMailQueue.get()
            #notice copy no pointer
	 
	    if ( self.conf['msgFilterMail']['mergeflag'] == 1 ):
		self.sendMergeMail(emailQueueNode)
		emailQueueNode=[]
	    else:
	    	if ( emailQueueNode['sendType'] == 1):
            		self.logObj.info("send msgFilter by Content mail begin!")
           		self.sendMailByContent( emailQueueNode )
            		self.logObj.info("send msgFilter by Content mail end!")
	    	else:
            		self.logObj.info("send msgFilter mail begin!")
            		self.sendMail( emailQueueNode )
            		self.logObj.info("send msgFilter mail end!")
            	emailQueueNode.clear()
            globalVariable.msgFilterMailQueue.task_done()
