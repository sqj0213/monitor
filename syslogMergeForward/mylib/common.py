#!/bin/env python
#coding=utf-8
import datetime,iso8601,time

def convertListToDict( _cf ):
    sectionsList = _cf.sections()
    retDict = {}
    for val1 in sectionsList:
        retDict[ val1 ] = dict( _cf.items( val1 ) )
    return retDict
def convertiso8601ToTimestamp( t ):
    #转换为datetime
    t1 = iso8601.parse_date(t)
    #转换为local_time
    t2 = t1.timetuple()
    #转换为时间戳
    t3 = time.mktime(t2)
    return t3