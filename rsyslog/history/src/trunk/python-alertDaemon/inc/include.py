import threading
import Queue

totalMSGCount = 0
totalEmailCount = 0
totalSMSCount = 0
syslogEmailNodeData = {}
#init smsm queue
syslogSMSNodeData = {}

#DECLARE email sms lock
#global mutexEmail,mutexSMS
#init sms email lock
#recive msg queue
reciveQueue = Queue.Queue()
emailQueue = Queue.Queue()
smsQueue = Queue.Queue()

#timer flag for save to actionQueue
timeFlag = False

priorityTag={'3':'error', '4':'warning'}

def setTimeFlag( _logObj ):

    _logObj.info( "timer is set timeFlag true" )
    timeFlag = True
