#!/bin/env python
#coding=utf8

import threading
from mylib import sendMail  as sendMail
import copy,time
from inc import include as globalVariable

class processSendmailQueue( threading.Thread ):

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
        self.alertEmailBodyTmpl = self.conf['sendmail']['mailbodytmpl']
        self.alertEmailTitleTmpl = self.conf['sendmail']['mailtitletmpl']
        threading.Thread.__init__( self )

    def stop( self ):
        self.stopFlag = True

    def writeLog( self, summary, detail ):

        return

    def sendMail( self, msgNode ):
        #alertData['500']['requestCount']=10
        #         ['www.gexing.com'][200]['requestCount']=5
        #

	print( msgNode )
        mailTitle = self.alertEmailTitleTmpl.replace( '__TITLE__', "[key filter alert]"+(" ".join(msgNode)) )
        mailBody = self.alertEmailBodyTmpl.replace( '__BODY__', " ".join(msgNode) )

        globalVariable.totalEmailCount += 1
        toMailList = self.toEmailList[ 'warning' ]
        gexingServiceMailObj =  sendMail.gexingServiceMail( self.fromEmailInfo[ 'fromEmail' ] , self.fromEmailInfo[ 'fromEmailPwd' ] )
        gexingServiceMailObj.send( mailTitle, mailBody, toMailList )
        self.logObj.info( "sendmail complete!to("+( '.'.join( toMailList ) )+")title("+mailTitle+")mailBody("+mailBody+")" )

    def run( self ):
        self.logObj.info( "sendmail thread start!" )
        while ( True ):
            if self.stopFlag:
                self.logObj.info( "sendmail thread is shutdown!" )
                break
                #notice this cmd will block
            emailQueueNode = globalVariable.sendmailQueue.get()

            #notice copy no pointer
            self.logObj.info("sendmail (key filter module) begin!")
            self.sendMail( emailQueueNode )
            self.logObj.info("sendmail (key filter module) end!")
            globalVariable.sendmailQueue.task_done()
            emailQueueNode = list()
