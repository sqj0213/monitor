import threading
import hashlib,copy
from inc import include as globalVariable

class dispatcherQueueNode( threading.Thread ):
    def __init__( self, conf, _logObj ):
        self.logObj = _logObj
        self.conf = conf
        self.stopFlag = False
        threading.Thread.__init__( self ) 

    def buildMsgID( self, level, title, msg ):
        return hashlib.md5( level + title + msg ).hexdigest()
    def stop( self ):
        self.stopFlag = True
    def writeLog( self, summary, detail ):
        return
    #rewrite thread main
    def run( self ):
        #global globalVariable.totalEmailCount,globalVariable.syslogEmailNodeData,globalVariable.mutexEmail
        #notice queue is null , block
        self.logObj.info( "dispatcher thread is start!" )
        while True:
            if self.stopFlag:
                self.logObj.info( "dispatcher thread is shutdown!" )
                break
            queueNode = globalVariable.reciveQueue.get()

            level = queueNode[ 0 ]
            queueNode[ 0 ] = globalVariable.priorityTag[ level ]
            queueNode[ 1 ] = queueNode[ 1 ]+"["+globalVariable.priorityTag[ level ]+"]"
            
            msgID = self.buildMsgID( queueNode[ 0 ], queueNode[ 1 ], queueNode[ 2 ] )
            #print self.syslogNodeData


            if ( queueNode[ 0 ] == "warning" or queueNode[ 0 ] == "error" ):#if email only sendmail else send sms
        
                if ( len( globalVariable.syslogEmailNodeData ) > self.conf[ 'queue' ][ 'recivequeuesize' ] ):
                    self.logObj.error( "info:recive is over quota(8196)\tlennodedata:"+len( globalVariable.syslogEmailNodeData )+"|totalCount:"+globalVariable.totalEmailCount+"|"+queueNode[ 1 ]+"|"+queueNode[ 2 ] );
                    continue
                if ( globalVariable.syslogEmailNodeData.has_key( msgID ) ):
                    globalVariable.syslogEmailNodeData[ msgID ][ 'msgCount' ] = globalVariable.syslogEmailNodeData[ msgID ][ 'msgCount' ] + 1
                else:
                   globalVariable. syslogEmailNodeData[ msgID ] = { 'msgCount':1, 'msgLevel':queueNode[ 0 ], 'title':queueNode[ 1 ], 'body':queueNode[ 2 ] }
                globalVariable.totalEmailCount = globalVariable.totalEmailCount + 1

            if   queueNode[ 0 ] == "error":     
                if ( globalVariable.syslogSMSNodeData.has_key( msgID ) ):
                    globalVariable.syslogSMSNodeData[ msgID ][ 'msgCount' ] = globalVariable.syslogSMSNodeData[ msgID ][ 'msgCount' ] + 1
                else:
                   globalVariable. syslogSMSNodeData[ msgID ] = { 'msgCount':1, 'msgLevel':queueNode[ 0 ], 'title':queueNode[ 1 ], 'body':queueNode[ 2 ] }
                globalVariable.totalSMSCount = globalVariable.totalSMSCount + 1
            
            if globalVariable.timeFlag:
                if ( globalVariable.emailQueue.qsize() >= int( self.conf[ 'queue' ][ 'actionqueuesize' ] ) ):
                    self.logObj.error( "notice action queue is full!" )
                else:
                    #notice consume thread must be clear dict for memory
                    globalVariable.emailQueue.put( copy.deepcopy( globalVariable. syslogEmailNodeData ) )
                    globalVariable.smsQueue.put( copy.deepcopy( globalVariable. syslogSMSNodeData ) )
                    globalVariable. syslogEmailNodeData.clear()
                    globalVariable. syslogSMSNodeData.clear()
                    self.logObj.info( "push action queue is success and clear current dict!" )
                globalVariable.timeFlag = False
