#!/bin/env python
#coding=utf8

import threading
from mylib import sendMail  as sendMail
import copy,time
from inc import include as globalVariable

class processEmailQueue( threading.Thread ):

    toEmailList = { 'warning':[], 'error':[] }
    fromEmailInfo = { 'fromEmail':'', 'fromEmailPwd':'' }
    msgBodyIndex = { 'warning':'warningBodyTmpl', 'error':'errorBodyTmpl', 'crit':'errorBodyTmpl' }
    conf = {}

    def __init__( self, conf, _logObj ):
        self.logObj = _logObj
        self.conf = conf
        self.stopFlag = False
        self.toEmailList[ 'warning' ] = self.conf[ 'email' ][ 'emailwarning' ].split( ',' )
        self.toEmailList[ 'error' ] = self.conf[ 'email' ][ 'emailerror' ].split( ',' )
        self.fromEmailInfo[ 'fromEmail' ] = self.conf[ 'email' ][ 'fromemail' ]
        self.fromEmailInfo[ 'fromEmailPwd' ] = self.conf[ 'email' ][ 'fromemailpwd' ]
        self.alertEmailBodyTmpl = self.conf['email']['alertbodytmpl']
        self.alertEmailTitleTmpl = self.conf['email']['alerttitletmpl']
        threading.Thread.__init__( self )


    def buildMailBody( self,  msgID, msgDetail ):
        retMsg = self.msgBodyIndex[ msgDetail[ 'msgLevel' ] ].replace( '__MSG__', msgDetail[ 'body' ] )
        retMsg = retMsg.replace( '__MSGCNT__', str( globalVariable.totalEmailCount ) ) 
	retMsg = retMsg.replace( '__REPCNT__', str( msgDetail[ 'msgCount' ] ) )
	retMsg = retMsg.replace( '__MSGID__', msgID )
	retMsg = retMsg.replace( '__TIME__', time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())) )
	globalVariable.totalEmailCount = globalVariable.totalEmailCount - msgDetail[ 'msgCount' ]
        return retMsg
    def stop( self ):
        self.stopFlag = True
    def writeLog( self, summary, detail ):

        return

    def sendMail( self, msgNode ):
        #alertData['500']['requestCount']=10
        #         ['www.gexing.com'][200]['requestCount']=5
        #
        """
        错误分布\n\t时间:__TIME__,主机名:__SERVERNAME__,错误次数:__REQUESTCNT__,状态码:__STATUS__
        """
        statusList = self.conf['processPolicy']['enablestatus']
        domainList = self.conf['processPolicy']['enableservername']
	tmpStatusCountTmpl = "_STATUS_:_COUNT_"
	mailBodyList =""
	mailTitleList=""
	statusCountList=""
	print msgNode
        for tmp in range( len( statusList ) ):

            status = statusList[tmp]
            if ( int(status) != 200 and int(status) !=304 ):
		if ( msgNode[status]['requestCount'] != 0 ):
			str1 = tmpStatusCountTmpl.replace('_STATUS_', str(status) )	
			str2 = str1.replace('_COUNT_', str(msgNode[status]['requestCount']))
			statusCountList = statusCountList + "|"+str2
                tmpBodyStr = ''

                for tmp1 in range( len(domainList)):
                    domain = domainList[tmp1]
                    if ( msgNode.has_key(domain) ):
                        if (msgNode[domain].has_key(status)):
                            if ( msgNode[domain][status]['requestCount'] != 0 ):
                                            tmpBodyStr1 = self.alertEmailBodyTmpl
                                            tmpBodyStr1 = tmpBodyStr1.replace('__SERVERNAME__', domain )
                                            tmpBodyStr1 = tmpBodyStr1.replace('__REQUESTCOUNT__', str(msgNode[domain][status]['requestCount']) )
                                            tmpBodyStr1 = tmpBodyStr1.replace('__STATUS__', str(status) )
                            else:
                                tmpBodyStr1 = ""
			    if ( len( tmpBodyStr1 ) != 0 ):
                            	tmpBodyStr += "<br>"+tmpBodyStr1
			    tmpBodyStr1 = ""
                        if ( msgNode[domain].has_key('200') ):
                            tmpStatus = '200'
                            if ( msgNode[domain][tmpStatus]['requestCount'] != 0 ):
                                            tmpBodyStr1 = self.alertEmailBodyTmpl
                                            tmpBodyStr1 = tmpBodyStr1.replace('__SERVERNAME__', domain )
                                            tmpBodyStr1 = tmpBodyStr1.replace('__REQUESTCOUNT__', str(msgNode[domain][tmpStatus]['requestCount']) )
                                            tmpBodyStr1 = tmpBodyStr1.replace('__STATUS__', str(tmpStatus) )
                            else:
                                tmpBodyStr1 = ""

			    if ( len( tmpBodyStr1 ) != 0 ):
                            	tmpBodyStr += "<br>"+tmpBodyStr1
			    tmpBodyStr1 = ""
                        if ( msgNode[domain].has_key('304') ):
                            tmpStatus = '304'
                            if ( msgNode[domain][tmpStatus]['requestCount'] != 0 ):
                                            tmpBodyStr1 = self.alertEmailBodyTmpl
                                            tmpBodyStr1 = tmpBodyStr1.replace('__SERVERNAME__', domain )
                                            tmpBodyStr1 = tmpBodyStr1.replace('__REQUESTCOUNT__', str(msgNode[domain][tmpStatus]['requestCount']) )
                                            tmpBodyStr1 = tmpBodyStr1.replace('__STATUS__', str(tmpStatus) )
                            else:
                                tmpBodyStr1 = ""

			    if ( len( tmpBodyStr1 ) != 0 ):
                            	tmpBodyStr += "<br>"+tmpBodyStr1

			    tmpBodyStr1 = ""

                        tmpBodyStr = tmpBodyStr.replace( '__DOMAIN__', domain )
                if ( len( tmpBodyStr ) != 0 ):
			mailBodyList = mailBodyList+ tmpBodyStr+"<br><br>"
			tmpBodyStr = ""
		else:
                	self.logObj.info( "this status has 0 error msg!" )

	if ( len( mailBodyList ) != 0 ):
                dateTimeStr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()-2))
		mailBodyList = mailBodyList.replace( '__TIME__', dateTimeStr )
		mailBodyList = "时间:"+dateTimeStr+"  "+mailBodyList
		mailTitleList =  self.alertEmailTitleTmpl.replace( '__STATUSCOUNT__',  statusCountList)
		diffStrTime = str(int(time.time())- globalVariable.lastAlertTime)
		mailTitleList =  mailTitleList.replace( '_MINUTE_',  diffStrTime)
                globalVariable.totalEmailCount += 1
                toMailList = self.toEmailList[ 'warning' ]
                gexingServiceMailObj =  sendMail.gexingServiceMail( self.fromEmailInfo[ 'fromEmail' ] , self.fromEmailInfo[ 'fromEmailPwd' ] )
                gexingServiceMailObj.send( mailTitleList, mailBodyList, toMailList )
                self.logObj.info( "send email complete!to("+( '.'.join( toMailList ) )+")title("+mailTitleList+")mailBody("+mailBodyList+")" )
        else:
        	self.logObj.info( "this status has 0 error msg!" )

    def run( self ):
        self.logObj.info( "send email thread start!" )
        while ( True ):
            if self.stopFlag:
                self.logObj.info( "send email thread is shutdown!" )
                break
                #notice this cmd will block
            emailQueueNode = globalVariable.emailQueue.get()
            #notice copy no pointer
            print emailQueueNode
            self.logObj.info("send mail begin!")
            self.sendMail( emailQueueNode )
            self.logObj.info("send mail end!")
            globalVariable.emailQueue.task_done()
            emailQueueNode.clear()
