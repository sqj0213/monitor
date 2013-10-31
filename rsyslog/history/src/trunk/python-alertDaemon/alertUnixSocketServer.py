import ConfigParser
import threading,os,sys
import logging as logObj

#timer lib
from mylib import myTimer as myTimer

#common function lib
from mylib import common
#socket daemon main 
from mylib import transactionFrame
#global variable and queue declare, timer reset func
from inc import include as globalVariable
#dispatcher main msg thread
from plugin import dispatcherQueueNode as dispatcherQueueNode
#send email thread
from plugin import processEmailQueue as processEmailQueue
#send sms thread
from plugin import processSMSQueue as processSMSQueue

#syslogNodeData = { 'msgID': { 'title':'title', 'body':'body','level':'warning', 'msgCount':0 } }
#init email queue



def help( argv ):
    if len( sys.argv ) != 2:
        print "start error: python alertUnixSocketServer.py unixSocketDaemon.ini"
        exit
    return

help( sys.argv )


#init configure 
cf = ConfigParser.ConfigParser()
cf.read( sys.argv[1] )
conf = common.convertListToDict( cf )
#format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
#init log obj
logObj.basicConfig(filename=conf[ 'log' ][ 'access' ],filemode='a+',level=logObj.INFO, format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s %(filename)s %(module)s %(lineno)d', datefmt='%Y-%m-%d %H:%M:%S' )
logObj.basicConfig(filename=conf[ 'log' ][ 'debug' ],filemode='a+',level=logObj.DEBUG, format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s %(filename)s %(module)s %(lineno)d', datefmt='%Y-%m-%d %H:%M:%S'  )
logObj.basicConfig(filename=conf[ 'log' ][ 'error' ],filemode='a+',level=logObj.ERROR, format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s %(filename)s %(module)s %(lineno)d', datefmt='%Y-%m-%d %H:%M:%S'  )

#build email object

#start timer set push action queue node flag is True
myTimer = myTimer.myTimer( int( conf[ 'queue' ][ 'buildactionqueueinterval' ] ), logObj )
myTimer.start()

#dispatcher reciveQueue node to email and sms queue
dispatcherQueueNodeObj = dispatcherQueueNode.dispatcherQueueNode( conf, logObj )
dispatcherQueueNodeObj.start()


#block emailQueue and sendmail this is single thread
processEmailQueueObj = processEmailQueue.processEmailQueue( conf, logObj )
processEmailQueueObj.start()


#block smsQueue this is single thread(system curl send sms)
processSMSQueueObj = processSMSQueue.processSMSQueue( conf, logObj )
processSMSQueueObj.start()



#build transaction frame object
server = transactionFrame.transactionFrame( conf, logObj )

#print conf
try:
    transactionFrame.asyncore.loop()

finally:
    if os.path.exists( conf[ 'socketInfo' ][ 'socket' ] ):
        os.unlink( conf[ 'socketInfo' ][ 'socket' ] )




