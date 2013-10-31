#!/bin/env python
#coding=utf8
import MySQLdb
from inc import include as globalVariable
import threading


"""
    conn=MySQLdb.connect(host='localhost',user='root',passwd='root',db='test',port=3306)
    cur=conn.cursor()
    cur.execute('select * from user')
    cur.close()
    conn.close()
"""
class processNginxNot200Queue(  threading.Thread ):
    DBObj = None
    def __init__(self, cf ):
        DBObj = MySQLdb.connect( cf['db']['dbhost'], cf['db']['dbuser'], cf['db']['dbpwd'], cf['db']['dbname'], cf['db']['dbport'] )

        pass
    def connDB(self):
        pass
    pass