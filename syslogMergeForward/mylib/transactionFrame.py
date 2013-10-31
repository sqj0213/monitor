#!/bin/env python
#coding=utf-8
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
        self.logObj.info( self.tmpStr )
        if os.path.exists( self.conf[ 'socketInfo' ][ 'socket' ] ):
            os.remove( self.conf[ 'socketInfo' ][ 'socket' ]  )

        self.close()
    def writeToQueue( self, queueNode ):
        #notice muti thread for this
        if globalVariable.reciveQueue.full():
            self.logObj.error( "recive msg protocol is invalid!" )
        else:
            globalVariable.reciveQueue.put( queueNode, False )
    def msgFilterDispatcher(self,msgNode):
        findFlag = False
        for k in self.conf['msgFilter']:
            filterStrArr = self.conf['msgFilter'][k]['filterStr']
            flag = True
            for j in range(len(filterStrArr)):
                if msgNode.find(filterStrArr[j]) == -1:
                    flag = False
            if ( flag ):
                findFlag = True
                self.logObj.info("recive msgFilter data and put into msgFilter queue!strNode("+str(msgNode)+") begin!")
		#若为定制发送，只发id即可
		if ( self.conf['msgFilter'][k]['sendType'] == 0 ):
                	globalVariable.msgFilterReciveQueue.put(k,False)
                	self.logObj.info("recive msgFilter (sendtype is 0 )data and put into msgFilter queue!strNode("+str(msgNode)+") end!")
		else:
			tmpVal = [k,msgNode]
                	globalVariable.msgFilterReciveQueue.put(tmpVal,False)
                	self.logObj.info("recive msgFilter (sendtype is 1) data and put into msgFilter queue!strNode("+str(msgNode)+") end!")
        return findFlag
    def handle_read( self ):
        reciveString = self.recv( int( self.conf[ 'socketInfo' ][ 'recivesize' ] ) )
        #self.logObj.info( reciveString )
        self.tmpStr = reciveString
        reciveStrList1 = reciveString.split(": ")
        """
print conf['msgFilter']
{'3c10c9e97fddae51e914ba17a787a57b': {'toMailList': ['sunquanjun@gexing.com', 'sqj0213@163.com'], 'serviceName': '"\xe5\xad\x98\xe5\x82\xa8', 'filterStr': ['pic.upload-server', 'fatal'], 'maxCount': '5'}, 
'50484c19f1afdaf3841a0d821ed393d2': {'toMailList': ['sunquanjun@gexing.com', 'sqj0213@163.com"'], 'serviceName': '\xe5\x85\xb6\xe5\xae\x83', 'filterStr': ['kernel'], 'maxCount': '3'}}
        """
        """
        if ( reciveStrList1[0].find("mysql-messages") != -1 or  reciveStrList1[0].find("redis-messages") != -1 or  reciveStrList1[0].find("webFront-messages") != -1 ):
            #Apr 12 14:28:57 cancer-hz4 mysql-messages: kernel: asdfasdf
            self.logObj.info(reciveString)
            globalVariable.sendmailQueue.put(reciveStrList1, False)
        """
        msgFilterFlag = self.msgFilterDispatcher(reciveString)
        if ( msgFilterFlag ):
            pass
        else:
            if ( len( reciveStrList1 ) >= 2 and len( reciveStrList1 ) <=3 ):
                tmpStr = reciveStrList1[1]
                tmpStr2 = reciveStrList1[0].split(" ")[4]
                if ( len( reciveStrList1 ) == 3 ):
                    tmpStr = tmpStr + "  "
                    tmpStr = tmpStr + reciveStrList1[2]
                reciveStrList = tmpStr.split( "  " )
                if ( len ( reciveStrList ) < 10 ):
                    self.logObj.info("recive msg protocol is invalid!strNode("+str(reciveString)+")")
                else:
                    if ( len( reciveStrList ) > 10 ):
                        reciveStrList[8] = reciveStrList[8] +"  " + reciveStrList[9]
                        reciveStrList[9] = reciveStrList[10]
                        #删除最多余的数据
                        reciveStrList.pop()
                    reciveStrList.insert(0,tmpStr2)

                    self.logObj.debug(reciveString)
                    #def processEmailInfo( level, title, msg, reciveSize=8196 ):
                    reciveStrList[globalVariable.protocalStatusColumn]=reciveStrList[globalVariable.protocalStatusColumn].replace("rc:","")
                    if len( reciveStrList ) == globalVariable.protocalDataColumnCount:
                        reciveStrList[globalVariable.protocalServerNameColumn]=reciveStrList[globalVariable.protocalServerNameColumn].replace("rc:","")
                        if ( reciveStrList[globalVariable.protocalServerNameColumn] in self.conf['processPolicy']['enableservername']):

                            if ( reciveStrList[globalVariable.protocalStatusColumn] in self.conf['processPolicy']['enablestatus'] ):
                                    self.writeToQueue( reciveStrList )
                            else:
                                    self.logObj.error( "recive msg protocol("+reciveStrList[globalVariable.protocalStatusColumn]+") is not in 200,500,502!" )
                        else:
                            self.logObj.error("this servername("+reciveStrList[globalVariable.protocalServerNameColumn]+") is not allowed")
                    else:
                            self.logObj.error( "recive msg protocol is invalid!strNode("+str(reciveString)+")" )
            else:
                self.logObj.error("recive nodeStr is invalid!str("+reciveString+")")

    def writable( self ):
        pass
        #self.logObj.info( "server is alive!" )


    def handle_write( self ):
        print 'handle_write'
        sent = self.send( self.buffer )
        self.buffer = self.buffer[sent:]
