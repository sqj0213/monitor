import asyncore, socket, os
import threading
from inc import include as globalVariable

class transactionFrame( asyncore.dispatcher ):

    def __init__( self, _conf, _logObj ):
        self.conf = _conf
        self.logObj = _logObj
        asyncore.dispatcher.__init__( self )
        self.create_socket( socket.AF_UNIX, socket.SOCK_DGRAM )
        self.set_reuse_addr()
        self.bind( self.conf[ 'socketInfo' ][ 'socket' ] )

    def handle_close( self ):
        self.logObj.info( "server shutdown!" )

        if os.path.exists( self.conf[ 'socketInfo' ][ 'socket' ] ):
            os.remove( self.conf[ 'socketInfo' ][ 'socket' ]  )

        self.close()
    def writeToQueue( self, queueNode ):
        #notice muti thread for this
        if globalVariable.reciveQueue.full():
            self.logObj.error( "recive msg protocol is invalid!" )
        else:
            globalVariable.reciveQueue.put( queueNode, False )
    def handle_read( self ):
        reciveString = self.recv( int( self.conf[ 'socketInfo' ][ 'recivesize' ] ) )
        self.logObj.info( reciveString )
        reciveStrList = reciveString.split( "|" )

        #def processEmailInfo( level, title, msg, reciveSize=8196 ):

        if len( reciveStrList ) == 3:
            self.writeToQueue( reciveStrList )
        else:
            self.logObj.error( "recive msg protocol is invalid!" )

    def writable( self ):
        pass
        #self.logObj.info( "server is alive!" )


    def handle_write( self ):
        print 'handle_write'
        sent = self.send( self.buffer )
        self.buffer = self.buffer[sent:]
