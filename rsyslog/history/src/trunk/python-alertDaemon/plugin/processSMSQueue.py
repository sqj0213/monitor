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


    def buildSMSBody( self,  msgID, msgDetail ):
        retMsg = self.msgTmpl.replace( '__MSG__', msgDetail[ 'body' ] )
        retMsg = retMsg.replace( '__MSGCNT__', str( globalVariable.totalSMSCount ) )
        retMsg = retMsg.replace( '__REPCNT__', str( msgDetail[ 'msgCount' ] ) )
        retMsg = retMsg.replace( '__TITLE__', msgDetail[ 'title' ] )
        retMsg = retMsg.replace( '__MSGID__', msgID )
        retMsg = retMsg.replace( '__TIME__', time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())) )
        globalVariable.totalSMSCount = globalVariable.totalSMSCount - msgDetail[ 'msgCount' ]
        return retMsg
    def stop( self ):
        self.stopFlag = True
    def reload( self ):
        self.reloadFlag = True

    def writeLog( self, summary, detail ):
        
        return

    def sendSMS( self, msgID, msgDetail ):
        smsMSG = self.buildSMSBody( msgID, msgDetail )
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
                
            for key,val in emailSMSNode.items():
                self.sendSMS( key, val )
			#notice this must be clear for mem
            emailSMSNode.clear()
