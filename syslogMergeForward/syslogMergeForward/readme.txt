
中转机日志合并与过滤

安装模块：
    easy_install iso8601

中转机rsyslog：
    过滤并合并500,502,200日志

nginx-access日志处理:
收集内容：
    1.200日志,500,502日志

syslog输入格式:
    gexing-access  cancer-hz5   www.gexing.com  2013-02-03T22:59:54+08:00  GET /api/index.php?callback=jQuery17203404815510426171_1359844346563&action=ajax_getLoginStatus&_=1359844347031 HTTP/1.1  /api/index.php  http://www.gexing.com/u/7180228/fs/6  182.234.64.129  122  200  Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; InfoPath.1)  0.004
计算规则：
    拆分200,500,502日志,并按照不同的规则登计算，然后回写rsyslog到中心机

syslog中转机输出:
    gexing-access  cancer-hz5   www.gexing.com  2013-02-03T22:59:54+08:00  GET /api/index.php?callback=jQuery17203404815510426171_1359844346563&action=ajax_getLoginStatus&_=1359844347031 HTTP/1.1  /api/index.php  http://www.gexing.com/u/7180228/fs/6  182.234.64.129  122  200  Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; InfoPath.1)  0.004


php-fpm-error日志处理:
输入样本:
../2013-02-01/18-cancer-ts11-php-fpm-error-error.log:php-fpm-error  cancer-ts11   [01-Feb-2013 18:07:54] WARNING: [pool www] child 21362 said into stderr: "NOTICE: PHP message: PHP Fatal error:  Uncaught exception 'Predis\Network\ConnectionException' with message 'Connection timed out' in phar:///data/www/htdocs/Abaca/ext/predis/predis_0.7.2.phar/Predis/Network/ConnectionBase.php:159"


程序启动:
/usr/bin/python /usr/local/gexing/alertDaemon/alertUnixSocketServer.py /usr/local/gexing/alertDaemon/conf/mergeLog.ini 1>/dev/null 2>/tmp/alertUnixSocketServer.err &
重启动:
ps ax|grep python|grep -v grep|awk '{print "kill -9 "$1}'|sh;rm -f /tmp/alertDaemon.sock 
/usr/bin/python /usr/local/gexing/alertDaemon/alertUnixSocketServer.py /usr/local/gexing/alertDaemon/conf/mergeLog.ini 1>/dev/null 2>/tmp/alertUnixSocketServer.err &

加入自启动:
/usr/bin/python /usr/local/gexing/alertDaemon/alertUnixSocketServer.py /usr/local/gexing/alertDaemon/conf/mergeLog.ini 1>/dev/null 2>/tmp/alertUnixSocketServer.err &

配置文件:
/usr/local/gexing/alertDaemon/conf/mergeLog.ini
日志:
/var/log/alertUnixSocketServer.log


日志收集、报警、排查、统计规划：

收集内容：
    前端日志：
        nginx
        php
        php慢日志
        dmesg

    存储日志：
        mysql慢日志
        fdfs日志

    应用日志：
        gearman_worker日志

    报警内容：
        状态码数量指定时间段内异常报警

    分析方式：
        用脚本提取报警时间段的所有日志排查

    统计内容：
        top时长处理请求信息
        合并后的

日志内容：
    数据库：合并后与top类的日志，入数据库，便于统计
    中心存储：合并后的nginx日志，所有的error日志，慢日志，messages日志，top日志，存储文件，保留时间：半年
    中转存储：nginx明细日志，所有的error日志，慢日志，messages日志,：保留时长:15天
    业务端：所有日志，保留时长:90天

中转机与中心机日志存储方式：

    appName:webFront-nginx-www.gexing.com-error webFront-nginx-www.gexing.com-info webFront-nginx-space.gexing.com-error webFront-nginx-space.gexing.com-info
    webFront-php-fpm-error webFront-php-fpm-slow webFront-php-fpm-admin webFront-messages

    /webFront/nginx/2013-12-21/11-www.gexing.com-error.log
                                       /11-www.gexing.com-info.log
                                       /11-space.gexing.com-error.log
                                       /11-space.gexing.com-info.log
             /php-fpm/2013-12-21/11-php-fpm-error.log
                                /11-php-fpm-slow.log
                                /11-php-fpm-admin.log
             /messages/2013-12-21/11-messages-info.log


    appName:mysql-master-error mysql-master-slow mysql-master-messages mysql-slave-error mysql-slave-slow mysql-slave-messages
    /mysql/master/2013-12-21/11-mysql-error.log
                            /11-mysql-slow.log
          /slave/2013-12-21/11-mysql-error.log
                           /11-mysql-slow.log
          /messages/2013-12-21/11-messages.log

    appName:redis-master-error redis-master-messages redis-slave-error redis-slave-messages
    /redis/master/redis-error/2013-12-21/11-redis-error.log
          /slave/redis-error/2013-12-21/11-redis-error.log
          /messages/2013-12-21/11-messages.log

    appName:gearman-gearman_worker-error gearman-gearman_worker-info gearman-gearmand gearman-gearmand-messages
    /gearman/gearman_worker/2013-12-21/11-gearman-worker-error.log
                                      /11-gearman-worker-info.log
            /gearmand/2013-12-21/11-gearmand.log
            /messages/2013-12-21/11-messages.log
    appName:

     storage-nginx-pic.upload.gexing.com-error storage-nginx-pic.upload.gexing.com-info storage-nginx-photo.gexing.com-error
     storage-nginx-photo.gexing.com-info storage-nginx-p.gexing.com-info  storage-nginx-a.gexing.com-info

     storage-php-fpm-error storage-php-fpm-slow storage-php-fpm-admin

     storage-cache-hz-squid-error storage-cache-ts-squid-error storage-cache-bj-squid-error storage-cache-hz-varnish-error

     storage-fdfs-storage storage-fdfs-tracker sorage-fdfs-fdhtd storage-fdfs-nginx-error storage-fdfs-nginx-info
     storage-messages
     /storage/nginx/2013-12-21/11-pic.upload.gexing.com-error.log
                                             /11-pic.upload.gexing.com-info.log
                                             /11-photo.gexing.com-error.log
                                             /11-photo.gexing.com-info.log
                                             /11-p.gexing.com-error.log
                                             /11-p.gexing.com-info.log
                                             /11-a.gexing.com-error.log
                                             /11-a.gexing.com-info.log

            /php-fpm/2013-12-21/11-php-fpm-error.log
                               /11-php-fpm-slow-info.log
                               /11-php-fpm-admin.log
            /cache/hz/squid/2013-12-21/11-squid-error.log
                  /ts/vanish/2013-12-21/11-varnish-error.log
                  /bj/vanish/2013-12-21/11-varnish-error.log

            /fdfs/storege/2013-12-21/11-fdfs-storage.log
                 /tracker/2013-12-21/11-fdfs-tracker.log
                 /fdhtd/2013-12-21/11-fdfs-fdhtd.log
                 /nginx/2013-12-21/11-fdfs-nginx-error.log
                                  /11-fdfs-nginx-info.log
            /messages/2013-12-21/11-messages.log



操作步骤：

一、前端机修改rsyslog配置:
    1.过滤掉所有状态码为200日志
    2.messsages日志回收
    3.webFront-nginx-www.gexing.com-error
    4.webFront-nginx-www.gexing.com-info
    5.webFront-nginx-space.gexing.com-error
    6.webFront-nginx-space.gexing.com-info
    7.webFront-php-fpm-error
    8.webFront-php-fpm-slow
    9.webFront-php-fpm-admin
    10.webFront-messages

    注意:
        1.由于php-fpm-error日志量非常大有部分的notice日志需要注意中转机的接收量与写磁盘的buffersize大小
        2.如何有效的去除未定义变量类的notice日志，需要调试
        3.中转机info与error日志重复记录的处理，有可能需要升级rsyslog

二、mysql的rsyslog配置：
    1.mysql-master配置rsyslog
        1.1.mysql-master-error
        1.2.mysql-master-slow
        1.3.mysql-master-messages
    2.mysql-slave配置rsyslog
        2.1.mysql-slave-error
        2.2.mysql-slave-slow
        2.3.mysql-slave-messages
三、redis的rsyslog配置:
    1.redis-master的rsyslog配置
        1.1redis-master-error
        1.2.redis-master-messages
    2.redis-slave的rsyslog配置
        2.1.redis-slave-error
        2.2.redis-slave-messages

四、gearman的rsyslog配置:
    1.gearmand的rsyslog的配置
        1.1.gearman-gearmand
        1.2.gearman-gearmand-messages
    2.gearman_worker的rsyslog配置
        2.1.gearman-gearman_worker-error
        2.2.gearman-gearman_worker-info
五、storage的rsyslog配置:
    1.上传与缩略的nginx部分rsyslog配置:
        1.1.storage-nginx-pic.upload.gexing.com-error
        1.2.storage-nginx-pic.upload.gexing.com-info
        1.3.storage-nginx-photo.gexing.com-error
        1.4.storage-nginx-photo.gexing.com-info
        1.5.storage-nginx-p.gexing.com-info
        1.6.storage-nginx-a.gexing.com-info
        1.7.storage-messages
    2.上传与缩略的php-fpm部分rsyslog配置:
        2.1.storage-php-fpm-error
        2.2.storage-php-fpm-slow
        2.3.storage-php-fpm-admin
        2.4.storage-messages
    3.cache部分的rsyslog配置：
        3.1.storage-cache-hz-squid-error
        3.2.storage-cache-ts-squid-error
        3.3.storage-cache-bj-squid-error
        3.4.storage-cache-hz-varnish-error
        3.5.storage-messages

    4.fdfs部分的rsyslog配置:
        4.1.storage-fdfs-storage
        4.2.storage-fdfs-tracker
        4.3.sorage-fdfs-fdhtd
        4.4.storage-fdfs-nginx-error
        4.5.storage-fdfs-nginx-info
        4.6.storage-messages

六、hz中转机配置:
    1.报警、合并与转发：
        1.1安装syslogMergeForward的程序
        1.2编辑配置文件（报警手机号与邮件地址，手机号，提醒的阀值）
        1.3编辑rsyslog部分，配置要报警提醒合并的规则（域名，过滤通道，归并后的日志转发中心机配置）
    2.webFront日志明细写磁盘配置：
        2.1前端nginx日志写磁盘的模板编辑
        2.2前端php-fpm日志写磁盘的模板编辑
        2.3前端messages日志写磁盘的编辑
    3.mysql日志写磁盘配置
        3.1.mysql-master配置
            3.1.1.mysql-master-error
            3.1.2.mysql-master-slow
        3.2.mysql-slave配置
            3.2.1.mysql-slave-error
            3.2.2.mysql-slave-slow
        3.3.mysql-slave-messages
    4.redis日志写磁盘配置
        4.1.redis-master-error配置:
        4.2.redis-slave-error配置:
        4.3.redis-messages配置:

    5.gearman日志写磁盘配置
        5.1.gearman_worker配置
            5.1.gearman-garman_worker-error
            5.2.gearman-gearman_worker-info
        5.2.gearman-gearmand日志配置
        5.3.gearman-gearmand-messages

    6.storage日志写磁盘配置:
        1.上传与缩略部分写磁盘配置:
            1.1.nginx部分:
                1.1.1.storage-nginx-pic.upload.gexing.com-error
                1.1.2.storage-nginx-pic.upload.gexing.com-info
                1.1.3.storage-nginx-photo.gexing.com-error
                1.1.4.storage-nginx-photo.gexing.com-info
                1.1.5.storage-nginx-p.gexing.com-info
                1.1.6.storage-nginx-a.gexing.com-info
            1.2.php-fpm部分:
                1.2.1.storage-php-fpm-error
                1.2.2.storage-php-fpm-slow
                1.2.3.storage-php-fpm-admin
        2.cache部分:
            2.1.storage-cache-hz-squid-error
            2.2.storage-cache-ts-squid-error
            2.3.storage-cache-bj-squid-error
            2.4.storage-cache-hz-varnish-error
        3.fdfs部分：
            3.1.storage-fdfs-storage
            3.2.storage-fdfs-tracker
            3.3.sorage-fdfs-fdhtd
            3.4.storage-fdfs-nginx-error
            3.5.storage-fdfs-nginx-info
        4.storage-messages
    7.中转机归并日志转发中心机配置：
        7.1.mergeLog转发配置
    8.中转机日志清除策略配置


七、中心机的配置：
    1.中心机日志清除策略配置






mkdir -p /data/site_log/webFront/nginx
mkdir -p /data/site_log/webFront/php-fpm
mkdir -p /data/site_log/webFront/messages
mkdir -p /data/site_log/mysql/master
mkdir -p /data/site_log/mysql/slave
mkdir -p /data/site_log/mysql/messages
mkdir -p /data/site_log/redis/master/redis-error
mkdir -p /data/site_log/redis/slave/redis-error
mkdir -p /data/site_log/redis/messages/




rsysog编译
./configure --sbindir=/sbin --sysconfdir=/etc --enable-mysql --enable-imfile --enable-imptcp --enable-imttcp --enable-impstats --enable-omprog --enable-omstdout --enable-pmlastmsg --enable-omuxsock  --enable-memcheck

