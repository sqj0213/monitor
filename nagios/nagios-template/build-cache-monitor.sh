#!/bin/sh
rm -f ./taskConf/*cache*.cfg
rm -f ./taskConf/*cache*.cfg.end
rm -f ./taskTmpl/localhost-cache-servicegroup.cfg
grep "\-_IP_"  ./taskTmpl/localhost-cache-monitor.cfg|awk '{print $2}'|uniq|awk 'BEGIN{FS="-_IP_-"}{if ( $0!="") print $2"::"$0}' >./taskTmpl/localhost-cache-servicegroup.cfg


cat ./ip/hz-cache-p.txt  |awk 'BEGIN{FS=":"}{print "sed -s s/_IP_/"$1"/g ./taskTmpl/localhost-cache-monitor.cfg |sed -s s/_PORT_/"$2"/g  >> ./taskConf/localhost-hz-cache.cfg"}'|sh
cat ./ip/hz-cache-a.txt  |awk 'BEGIN{FS=":"}{print "sed -s s/_IP_/"$1"/g ./taskTmpl/localhost-cache-monitor.cfg |sed -s s/_PORT_/"$2"/g  >> ./taskConf/localhost-hz-cache.cfg"}'|sh
cat ./ip/hz-cache-p.txt  |awk 'BEGIN{FS=":"}{print "sed -s s/_IP_/"$1"/g ./taskTmpl/localhost-cache-servicegroup.cfg|sed -s s/_PORT_/"$2"/g   >> ./taskConf/localhost-cache-servicegroup.cfg"}'|sh
cat ./ip/hz-cache-a.txt  |awk 'BEGIN{FS=":"}{print "sed -s s/_IP_/"$1"/g ./taskTmpl/localhost-cache-servicegroup.cfg|sed -s s/_PORT_/"$2"/g   >> ./taskConf/localhost-cache-servicegroup.cfg"}'|sh

sed -i 's/-172.16.3./hz/g' ./taskConf/localhost-hz-*.cfg
sed -i 's/-122.225.115./hz/g' ./taskConf/localhost-hz-*.cfg

cat ./ip/ts-cache-ap.txt  |awk 'BEGIN{FS=":"}{print "sed -s s/_IP_/"$1"/g ./taskTmpl/localhost-cache-monitor.cfg|sed -s s/_PORT_/"$2"/g   >> ./taskConf/localhost-ts-cache-ap.cfg"}'|sh
cat ./ip/ts-cache-ap.txt  |awk 'BEGIN{FS=":"}{print "sed -s s/_IP_/"$1"/g ./taskTmpl/localhost-cache-servicegroup.cfg|sed -s s/_PORT_/"$2"/g   >> ./taskConf/localhost-cache-servicegroup.cfg"}'|sh

sed -i 's/-60.2.235./ts/g' ./taskConf/localhost-ts-*.cfg


sed -i 's/-60.2.235./localhost,ts/g' ./taskConf/localhost-cache-servicegroup.cfg
sed -i 's/-172.16.3./localhost,hz/g' ./taskConf/localhost-cache-servicegroup.cfg
sed -i 's/-122.225.115./localhost,hz/g' ./taskConf/localhost-cache-servicegroup.cfg

php ./convert.php ./taskConf/localhost-cache-servicegroup.cfg >./taskConf/localhost-cache-servicegroup.cfg.end
/bin/rm -f  ./taskConf/localhost-cache-servicegroup.cfg
mv  ./taskConf/localhost-cache-servicegroup.cfg.end  ./taskConf/localhost-cache-servicegroup.cfg
