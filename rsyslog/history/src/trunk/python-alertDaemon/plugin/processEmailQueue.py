import threading
from mylib import sendMail  as sendMail
import copy,time
from inc import include as globalVariable

class processEmailQueue( sendMail.gexingServiceMail, threading.Thread ):

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
        self.msgBodyIndex[ 'warning' ] = self.conf[ 'email' ][ 'warningbodytmpl' ]
        self.msgBodyIndex[ 'error' ] = self.conf[ 'email' ][ 'errorbodytmpl' ]
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

    def sendMail( self, msgID, msgDetail ):
        mailTitle = msgDetail[ 'title' ]
        mailBody = self.buildMailBody( msgID, msgDetail )
        toMailList = self.toEmailList[ msgDetail[ 'msgLevel' ] ]
        gexingServiceMailObj =  sendMail.gexingServiceMail( self.fromEmailInfo[ 'fromEmail' ] , self.fromEmailInfo[ 'fromEmailPwd' ] )
        gexingServiceMailObj.send( mailTitle, mailBody, toMailList )
        self.logObj.info( "send email complete!to("+( '.'.join( toMailList ) )+")title("+mailTitle+")mailBody("+mailBody+")" )

    def run( self ):
        self.logObj.info( "send email thread start!" )
        while ( True ):
            if self.stopFlag:
                self.logObj.info( "send email thread is shutdown!" )
                break
            #notice this cmd will block
            emailQueueNode = globalVariable.emailQueue.get()
            #notice copy no pointer
                
            for key,val in emailQueueNode.items():
                self.sendMail( key, val )
            globalVariable.emailQueue.task_done()
            emailQueueNode.clear()
