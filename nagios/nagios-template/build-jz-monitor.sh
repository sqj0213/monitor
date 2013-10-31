#!/bin/sh
rm -f ./taskConf/*.cfg
rm -f ./taskConf/*.cfg.end
rm -f ./taskTmpl/localhost-servicegroup.cfg
grep "\-_IP_"  ./taskTmpl/localhost-browser-www-monitor.cfg|awk '{print $2}'|uniq|awk 'BEGIN{FS="-_IP_-"}{if ( $0!="") print $2"::"$0}' >./taskTmpl/localhost-servicegroup.cfg
grep "\-_IP_"  ./taskTmpl/localhost-browser-z-monitor.cfg|awk '{print $2}'|uniq|awk 'BEGIN{FS="-_IP_-"}{if ( $0!="") print $2"::"$0}' >>./taskTmpl/localhost-servicegroup.cfg
grep "\-_IP_"  ./taskTmpl/localhost-mobile-api-monitor.cfg|awk '{print $2}'|uniq|awk 'BEGIN{FS="-_IP_-"}{if ( $0!="") print $2"::"$0}' >>./taskTmpl/localhost-servicegroup.cfg
grep "\-_IP_"  ./taskTmpl/localhost-browser-sso-monitor.cfg|awk '{print $2}'|uniq|awk 'BEGIN{FS="-_IP_-"}{if ( $0!="") print $2"::"$0}' >>./taskTmpl/localhost-sso-servicegroup.cfg

cat ./ip/hz-web.txt  |awk 'BEGIN{FS=":"}{print "sed -s s/_IP_/"$1"/g ./taskTmpl/localhost-browser-www-monitor.cfg |sed -s s/_PORT_/"$2"/g  >> ./taskConf/localhost-hz-browser-www.cfg"}'|sh
cat ./ip/hz-web.txt  |awk 'BEGIN{FS=":"}{print "sed -s s/_IP_/"$1"/g ./taskTmpl/localhost-browser-z-monitor.cfg|sed -s s/_PORT_/"$2"/g   >> ./taskConf/localhost-hz-browser-z.cfg"}'|sh
cat ./ip/hz-web.txt  |awk 'BEGIN{FS=":"}{print "sed -s s/_IP_/"$1"/g ./taskTmpl/localhost-mobile-api-monitor.cfg|sed -s s/_PORT_/"$2"/g   >> ./taskConf/localhost-hz-mobile-api.cfg"}'|sh
cat ./ip/hz-web.txt  |awk 'BEGIN{FS=":"}{print "sed -s s/_IP_/"$1"/g ./taskTmpl/localhost-servicegroup.cfg|sed -s s/_PORT_/"$2"/g   >> ./taskConf/localhost-servicegroup.cfg"}'|sh
sed -i 's/-172.16.3./hz/g' ./taskConf/localhost-hz-*.cfg

cat ./ip/ts-web.txt  |awk 'BEGIN{FS=":"}{print "sed -s s/_IP_/"$1"/g ./taskTmpl/localhost-browser-www-monitor.cfg|sed -s s/_PORT_/"$2"/g   >> ./taskConf/localhost-ts-browser-www.cfg"}'|sh
cat ./ip/ts-web.txt  |awk 'BEGIN{FS=":"}{print "sed -s s/_IP_/"$1"/g ./taskTmpl/localhost-browser-z-monitor.cfg|sed -s s/_PORT_/"$2"/g   >> ./taskConf/localhost-ts-browser-z.cfg"}'|sh
cat ./ip/ts-web.txt  |awk 'BEGIN{FS=":"}{print "sed -s s/_IP_/"$1"/g ./taskTmpl/localhost-mobile-api-monitor.cfg|sed -s s/_PORT_/"$2"/g   >> ./taskConf/localhost-ts-mobile-api.cfg"}'|sh
cat ./ip/ts-web.txt  |awk 'BEGIN{FS=":"}{print "sed -s s/_IP_/"$1"/g ./taskTmpl/localhost-servicegroup.cfg|sed -s s/_PORT_/"$2"/g   >> ./taskConf/localhost-servicegroup.cfg"}'|sh

sed -i 's/-172.16.5./ts/g' ./taskConf/localhost-ts-*.cfg

cat ./ip/bj-sso.txt  |awk 'BEGIN{FS=":"}{print "sed -s s/_IP_/"$1"/g ./taskTmpl/localhost-browser-sso-monitor.cfg|sed -s s/_PORT_/"$2"/g   >> ./taskConf/localhost-bj-browser-sso.cfg"}'|sh
cat ./ip/bj-sso.txt  |awk 'BEGIN{FS=":"}{print "sed -s s/_IP_/"$1"/g ./taskTmpl/localhost-sso-servicegroup.cfg|sed -s s/_PORT_/"$2"/g   >> ./taskConf/localhost-servicegroup.cfg"}'|sh
sed -i 's/-172.16.1./bj/g' ./taskConf/localhost-bj-*.cfg

sed -i 's/-172.16.5./localhost,ts/g' ./taskConf/localhost-servicegroup.cfg
sed -i 's/-172.16.3./localhost,hz/g' ./taskConf/localhost-servicegroup.cfg
sed -i 's/-172.16.1./localhost,bj/g' ./taskConf/localhost-servicegroup.cfg

php ./convert.php ./taskConf/localhost-servicegroup.cfg >./taskConf/localhost-servicegroup.cfg.end
/bin/rm -f  ./taskConf/localhost-servicegroup.cfg
mv  ./taskConf/localhost-servicegroup.cfg.end  ./taskConf/localhost-servicegroup.cfg
