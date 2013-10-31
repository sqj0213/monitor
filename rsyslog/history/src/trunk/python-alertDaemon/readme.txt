目前只支持daemon方式运行
特性:
支持邮件与短信提醒
邮件与短信提醒周期为5分钟，对于重复的消息进行合并，并统计重复的次数
问题:
目前没有成为真正的daemon方式运行


程序启动:
/usr/bin/python /usr/local/gexing/alertDaemon/alertUnixSocketServer.py /usr/local/gexing/alertDaemon/conf/unixSocketDaemon.ini 1>/dev/null 2>/tmp/alertUnixSocketServer.err &
重启动:
ps ax|grep python|grep -v grep|awk '{print "kill -9 "$1}'|sh;rm -f /tmp/alertDaemon.sock 
/usr/bin/python /usr/local/gexing/alertDaemon/alertUnixSocketServer.py /usr/local/gexing/alertDaemon/conf/unixSocketDaemon.ini 1>/dev/null 2>/tmp/alertUnixSocketServer.err &

加入自启动:
/usr/bin/python /usr/local/gexing/alertDaemon/alertUnixSocketServer.py /usr/local/gexing/alertDaemon/conf/unixSocketDaemon.ini 1>/dev/null 2>/tmp/alertUnixSocketServer.err &

配置文件:
/usr/local/gexing/alertDaemon/conf/unixSocketDaemon.ini
日志:
/var/log/alertUnixSocketServer.log
