import threading, time
from inc import include as globalVariable
class myTimer( threading.Thread ):
    def __init__( self, interval, logObj ):
        threading.Thread.__init__( self )
        self.logObj = logObj
        self.stopFlag = False
        self.interval = interval
    def stop( self ):
        self.stopFlag = True
    def run( self ):
        while True:
            if self.stopFlag:
                break
            self.logObj.info( "timer is set timeFlag true" )
            globalVariable.timeFlag = True
            time.sleep( self.interval )