#!/bin/env python
#coding=utf-8
import threading
import hashlib,copy
import syslog
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

    def initMergeLogData(self):
        #alertData['500']['requestCount']=10
        #         ['www.gexing.com'][200]['requestCount']=5
        #
        globalVariable.protocalData = {}
        self.logObj.info('init merge log data struct begin!')
        serverNameList = self.conf['processPolicy']['enableservername']
        statusList = self.conf['processPolicy']['enablestatus']
        globalVariable.alertData['alertFlag'] = False
        for val in range( len(serverNameList)):
            if ( not globalVariable.protocalData.has_key(serverNameList[val])):
                globalVariable.protocalData[serverNameList[val]]={}
                globalVariable.alertData[serverNameList[val]]={}

            for val1 in range( len(statusList ) ):
                globalVariable.protocalData[serverNameList[val]][statusList[val1]] = {}
                if ( val1 != 200 and val1 !=304 ):
                    globalVariable.alertData[statusList[val1]]={'requestCount':0}
                globalVariable.alertData[serverNameList[val]][statusList[val1]]={'requestCount':0}
        self.logObj.info('init merge log data struct end!')

    def writeRsyslog(self):
        syslog.openlog("mergeLog", syslog.LOG_LOCAL6)
        #data['www.gexing.com']['200']['hz5']['/index.php']={'www.gexing.com',}
        #logTmplStr=__SERVERNAME__  __HOSTNAME__  __URI__  REQUESTCOUNT__  __HTTPBODYSIZE__  __HTTPSTATUS__  __HTTPREQUESTTIME__  __TIMEINTERVAL__
        serverNameList = self.conf['processPolicy']['enableservername']
        statusList = self.conf['processPolicy']['enablestatus']
        for val in range(len( serverNameList )):
            serverName = serverNameList[val]
            for val1 in range( len(statusList ) ):
                status = statusList[val1]
                tmpLogStr = self.conf['processPolicy']['logtmplstr']
                logStr = ""
                print globalVariable.protocalData
                if ( len( globalVariable.protocalData[serverName][status] ) != 0 ):
                    #遍历hostName
                    for k1,v1 in globalVariable.protocalData[serverName][status].items():
                        #遍历uri
                        for k,v in v1.items():
                            logStr = tmpLogStr.replace('__SERVERNAME__', v['serverName'] )
                            logStr = logStr.replace('__HOSTNAME__', v['hostName'])
                            logStr = logStr.replace('__URI__', v['uri'])
                            logStr = logStr.replace('__REQUESTCOUNT__', str(v['requestCount']))
                            logStr = logStr.replace('__HTTPBODYSIZE__', str(v['httpBodySize']))
                            logStr = logStr.replace('__HTTPSTATUS__', v['httpStatus'])
                            logStr = logStr.replace('__HTTPREQUESTTIME__', str(v['requestTime']))
                            logStr = logStr.replace('__TIMEINTERVAL__', str(v['timeInterval']))
                            syslog.syslog(syslog.LOG_INFO,logStr)
                else:
                    self.logObj.info('write rsyslog queue is null nothing to do!')
                globalVariable.protocalData[serverName][status] = {}
        syslog.closelog()
        return
    def mergeFilterMsgLog(self,nodeData):
        
        pass
    def mergeLog( self, nodeData ):
        if nodeData[globalVariable.protocalStatusColumn] in self.conf['processPolicy']['enablestatus']:
            status = nodeData[globalVariable.protocalStatusColumn]
            serverName = nodeData[globalVariable.protocalServerNameColumn]
            hostName = nodeData[globalVariable.protocalHostNameColumn]
            uri = nodeData[globalVariable.protocalUriColumn]

            if ( not globalVariable.protocalData[serverName][status].has_key(hostName)):
                globalVariable.protocalData[serverName][status]= {hostName:{}}
                globalVariable.alertData[serverName][status]['requestCount'] = 0

            if ( not globalVariable.protocalData[serverName][status][hostName].has_key(uri) ):
                globalVariable.protocalData[serverName][status][hostName][uri]={}
                globalVariable.protocalData[serverName][status][hostName][uri]['serverName'] = nodeData[1]
                globalVariable.protocalData[serverName][status][hostName][uri]['hostName'] = nodeData[0]
                globalVariable.protocalData[serverName][status][hostName][uri]['uri'] = nodeData[4]

                globalVariable.protocalData[serverName][status][hostName][uri]['requestCount'] = 1
                globalVariable.protocalData[serverName][status][hostName][uri]['httpBodySize'] = float(nodeData[7])
                globalVariable.protocalData[serverName][status][hostName][uri]['requestTime'] = float(nodeData[10])

                globalVariable.protocalData[serverName][status][hostName][uri]['timeInterval'] = globalVariable.currentTime
                globalVariable.protocalData[serverName][status][hostName][uri]['httpStatus'] = status

            else:#data['www.gexing.com']['200']['hz5']['/index.php']={'www.gexing.com',}
                globalVariable.protocalData[serverName][status][hostName][uri]['requestCount'] += 1
                globalVariable.protocalData[serverName][status][hostName][uri]['httpBodySize'] += float(nodeData[7])
                globalVariable.protocalData[serverName][status][hostName][uri]['requestTime'] += float(nodeData[10])

            globalVariable.alertData[serverName][status]['requestCount'] += 1

            if int(status) != 200 and int(status)!= 304:
                #非正常状态值加1
                globalVariable.alertData[status]['requestCount'] += 1
                #若非正常状态值大于配置的值时把报警标志位置为报警状态
                if globalVariable.alertData[status]['requestCount'] > int(self.conf['processPolicy']['alertcountperhostname']):
                    self.logObj.info('set log flag is true!')
                    globalVariable.alertData['alertFlag'] = True
                else:
                    globalVariable.alertData['alertFlag'] = False
        else:
            self.logObj.error('http status not record!')

    #rewrite thread main
    def run( self ):
        #global globalVariable.totalEmailCount,globalVariable.syslogEmailNodeData,globalVariable.mutexEmail
        #notice queue is null , block
        self.logObj.info( "dispatcher thread is start!" )
        self.initMergeLogData()
        print globalVariable.protocalData
        statusList = self.conf['processPolicy']['enablestatus']
        while True:
            if self.stopFlag:
                self.logObj.info( "dispatcher thread is shutdown!" )
                break
            queueNode = globalVariable.reciveQueue.get()

            self.mergeLog(queueNode)
            #hostname_uri_200
	    #若报警标志为需要报警则把要报警信息推入报警队列
            if globalVariable.alertData['alertFlag']:
                self.logObj.info('recive nginx error count up 10 and push msg to email&sms queue begin!')
                globalVariable.emailQueue.put(copy.deepcopy(globalVariable.alertData))
                globalVariable.smsQueue.put(copy.deepcopy(globalVariable.alertData))

                serverNameList = self.conf['processPolicy']['enableservername']
                statusList = self.conf['processPolicy']['enablestatus']
                for val in range( len(serverNameList)):
                    for val1 in range( len(statusList ) ):
                        globalVariable.protocalData[serverNameList[val]][statusList[val1]] = {}
                        if ( int(val1) != 200 and  int(val1) !=304 ):
                            globalVariable.alertData[statusList[val1]]={'requestCount':0}
                        globalVariable.alertData[serverNameList[val]][statusList[val1]]={'requestCount':0}

                globalVariable.alertData['alertFlag']=False
                self.logObj.info('recive nginx error count up 10 and push msg to email&sms queue end!')
            #若报警定时器为到时状态，则重置报警消息,重新计数
            if globalVariable.timeSendMsgFlag:
                self.logObj.info('send msg period is true and reset send msg period flag begin!')
                serverNameList = self.conf['processPolicy']['enableservername']
                statusList = self.conf['processPolicy']['enablestatus']
                for val in range( len(serverNameList)):
                    for val1 in range( len(statusList ) ):
                        if ( int(val1) != 200 and int(val1) !=304 ):
                            globalVariable.alertData[statusList[val1]]={'requestCount':0}
                        globalVariable.alertData[serverNameList[val]][statusList[val1]]={'requestCount':0}

                globalVariable.alertData['alertFlag']=False
                globalVariable.timeSendMsgFlag = False
                self.logObj.info('send msg period is true and reset send msg period flag end!')


            #放入action队列
            if globalVariable.timeWriteRsyslogFlag:
                self.logObj.info('push merge log into local syslog begin!')
                self.writeRsyslog()
                self.logObj.info('push merge log into local syslog end!')
                globalVariable.timeWriteRsyslogFlag = False
