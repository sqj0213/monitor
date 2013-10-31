#浏览器请求接口监控－空间接口
#取个人中心访客接口：
#php ./checkCurlHttp.php -H z.gexing.com -U "http://127.0.0.1/?abaca_module=friend&abaca_action=api_get_userlist&uid=6336831&index=0&p=1&t=1364205331178" -Tc 5 -Tw 2 -G "nickname" -OUTMSGPRE "browser-z-xhr-api_get_userlist"
#task name: browser-z-xhr-api_get_userlist
check_http  -H z.gexing.com -I 123.103.21.144 -u "/?abaca_module=friend&abaca_action=api_get_userlist&uid=6336831&index=0&p=1&t=1364205331178" --string="nickname" -c 5 -w 2 

#个人中心谁在聊接口：
#php ./checkCurlHttp.php -H z.gexing.com -U "http://127.0.0.1/?abaca_module=user&abaca_action=api_justsay_user_list&page=1&t=1364205619323" -Tc 5 -Tw 2  -G "nickname" -OUTMSGPRE "browser-z-xhr-api_justsay_user_list"
#task name: browser-z-xhr-api_justsay_user_list
check_http  -H z.gexing.com -I 123.103.21.144 -u "/?abaca_module=friend&abaca_action=api_get_userlist&uid=6336831&index=0&p=1&t=1364205331178" --string="nickname" -c 5 -w 2 

#个人中心首页接口：
#php ./checkCurlHttp.php -H z.gexing.com -U "http://127.0.0.1/u/6336831" -Tc 5 -Tw 2 -Soc 15000 -OUTMSGPRE "browser-z-userhome"
#task name:browser-z-userhome
check_http  -H z.gexing.com -I 123.103.21.144 -u "/u/6336831" -c 5 -w 2 --pagesize=40000:1024000

#发起群聊接口：不上线
#http://z.gexing.com/index.php?abaca_module=mood&abaca_action=api_publish_mood&t=1364206246919_8223


































#!/bin/sh
#浏览器请求接口监控－日记鲜花鸡蛋接口
#task name:browser-xhr-riji-ajax_getPostStatus
check_http  -H www.gexing.com -I 123.103.21.144 -u "/api/index.php?callback=jQuery17202293667936584859_1364202527719&action=ajax_getPostStatus&postIds=8678866%2C8678854%2C8678826%2C8678824%2C8678806%2C8678788%2C8678773%2C8678735%2C8678712&sucaiType=riji&_=1364202528987&tag_user=&allowComment=1&ztid=&type=shaitu" --string="ok" -c 5 -w 2 

#浏览器请求接口-搜索接口
#签名搜索接口：
#php ./checkCurlHttp.php -H www.gexing.com -U "http://127.0.0.1/qqqianming/s/女生" -Tc 5 -Tw 2 -Soc 80000 -OUTMSGPRE "browser-search-qqqianming"
#task name:browser-search-qqqianming
check_http  -H www.gexing.com -I 123.103.21.144 -u "/qqqianming/s/女生" --string="ok" -c 5 -w 2 --pagesize=80000:1024000
#qq头像搜索接口：
#php ./checkCurlHttp.php -H www.gexing.com  -U "http://127.0.0.1/qqtouxiang/s/%E7%94%B7%E4%BA%BA%E5%A5%B3%E4%BA%BA" -Tc 5 -Tw 2 -Soc 35000 -OUTMSGPRE "browser-search-qqtouxiang"
#task name: browser-search-qqtouxiang
check_http  -H www.gexing.com -I 123.103.21.144 -u "/qqtouxiang/s/%E7%94%B7%E4%BA%BA%E5%A5%B3%E4%BA%BA" -c 5 -w 2 --pagesize=35000:1024000
#自拍搜索接口:
#php ./checkCurlHttp.php -H www.gexing.com -U "http://127.0.0.1/list.zipai.php?callback=jQuery172046277252535455693_1364366634703&p=1&type=latest&tag=&order=new&action=ajaxGetPost" -Tc 5 -Tw 2 -Soc 5500 -OUTMSGPRE "browser-search-zipai"
#task name:browser-search-zipai
check_http  -H www.gexing.com -I 123.103.21.144 -u "/list.zipai.php?callback=jQuery172046277252535455693_1364366634703&p=1&type=latest&tag=&order=new&action=ajaxGetPost" -c 5 -w 2 --pagesize=5500:1024000
#日记搜索接口：
#task name:browser-search-riji
#php ./checkCurlHttp.php -H www.gexing.com -U "http://127.0.0.1/riji/s/%E5%BF%83%E6%83%85" -Tc 5 -Tw 2 -Soc 40000 -OUTMSGPRE "browser-search-riji"
check_http  -H www.gexing.com -I 123.103.21.144 -u "/riji/s/%E5%BF%83%E6%83%85" -c 5 -w 2 --pagesize=40000:1024000
#qq分组搜索接口：
#php ./checkCurlHttp.php -H www.gexing.com -U "http://127.0.0.1/qqfenzu/s/%E6%83%85%E4%BE%A3" -Tc 5 -Tw 2 -Soc 70000 -OUTMSGPRE "browser-search-qqfengzu"
#task name:browser-search-qqfengzu
check_http  -H www.gexing.com -I 123.103.21.144 -u "/qqfenzu/s/%E6%83%85%E4%BE%A3" -c 5 -w 2 --pagesize=70000:1024000

#qq皮肤搜索接口:
#php ./checkCurlHttp.php -H www.gexing.com -U "http://127.0.0.1/qqpifu/s/%E7%A4%BE%E4%BC%9A" -Tc 5 -Tw 2 -Soc 35000 -OUTMSGPRE "browser-search-qqpifu"
#task name: browser-search-qqpifu
check_http  -H www.gexing.com -I 123.103.21.144 -u "/qqpifu/s/%E7%A4%BE%E4%BC%9A" -c 5 -w 2 --pagesize=35000:1024000
#空间皮肤搜索接口：
#php ./checkCurlHttp.php -H www.gexing.com -U "http://127.0.0.1/pifu/s/%E5%B0%8F%E6%B8%85%E6%96%B0" -Tc 5 -Tw 2 -Soc 50000  -OUTMSGPRE "browser-search-kongjianpifu"
#task name:browser-search-kongjianpifu
check_http  -H www.gexing.com -I 123.103.21.144 -u "/pifu/s/%E5%B0%8F%E6%B8%85%E6%96%B0" -c 5 -w 2 --pagesize=50000:1024000

#壁纸搜索接口：
#php ./checkCurlHttp.php -H www.gexing.com -U "http://127.0.0.1/bizhi/s/%E9%A3%8E%E6%99%AF" -Tc 5 -Tw 2 -Soc 50000 -OUTMSGPRE "browser-search-bizhi"
#task name:browser-search-bizhi
check_http  -H www.gexing.com -I 123.103.21.144 -u "/bizhi/s/%E9%A3%8E%E6%99%AF" -c 5 -w 2 --pagesize=50000:1024000




















#!/bin/sh
#浏览器请求接口监控－日记鲜花鸡蛋接口
#task name:browser-xhr-riji-ajax_getPostStatus
check_http  -H www.gexing.com -I 123.103.21.144 -u "/api/index.php?callback=jQuery17202293667936584859_1364202527719&action=ajax_getPostStatus&postIds=8678866%2C8678854%2C8678826%2C8678824%2C8678806%2C8678788%2C8678773%2C8678735%2C8678712&sucaiType=riji&_=1364202528987&tag_user=&allowComment=1&ztid=&type=shaitu" --string="ok" -c 5 -w 2 

#浏览器请求接口-搜索接口
#签名搜索接口：
#php ./checkCurlHttp.php -H www.gexing.com -U "http://127.0.0.1/qqqianming/s/女生" -Tc 5 -Tw 2 -Soc 80000 -OUTMSGPRE "browser-search-qqqianming"
#task name:browser-search-qqqianming
check_http  -H www.gexing.com -I 123.103.21.144 -u "/qqqianming/s/女生" --string="ok" -c 5 -w 2 --pagesize=80000:1024000
#qq头像搜索接口：
#php ./checkCurlHttp.php -H www.gexing.com  -U "http://127.0.0.1/qqtouxiang/s/%E7%94%B7%E4%BA%BA%E5%A5%B3%E4%BA%BA" -Tc 5 -Tw 2 -Soc 35000 -OUTMSGPRE "browser-search-qqtouxiang"
#task name: browser-search-qqtouxiang
check_http  -H www.gexing.com -I 123.103.21.144 -u "/qqtouxiang/s/%E7%94%B7%E4%BA%BA%E5%A5%B3%E4%BA%BA" -c 5 -w 2 --pagesize=35000:1024000
#自拍搜索接口:
#php ./checkCurlHttp.php -H www.gexing.com -U "http://127.0.0.1/list.zipai.php?callback=jQuery172046277252535455693_1364366634703&p=1&type=latest&tag=&order=new&action=ajaxGetPost" -Tc 5 -Tw 2 -Soc 5500 -OUTMSGPRE "browser-search-zipai"
#task name:browser-search-zipai
check_http  -H www.gexing.com -I 123.103.21.144 -u "/list.zipai.php?callback=jQuery172046277252535455693_1364366634703&p=1&type=latest&tag=&order=new&action=ajaxGetPost" -c 5 -w 2 --pagesize=5500:1024000
#日记搜索接口：
#task name:browser-search-riji
#php ./checkCurlHttp.php -H www.gexing.com -U "http://127.0.0.1/riji/s/%E5%BF%83%E6%83%85" -Tc 5 -Tw 2 -Soc 40000 -OUTMSGPRE "browser-search-riji"
check_http  -H www.gexing.com -I 123.103.21.144 -u "/riji/s/%E5%BF%83%E6%83%85" -c 5 -w 2 --pagesize=40000:1024000
#qq分组搜索接口：
#php ./checkCurlHttp.php -H www.gexing.com -U "http://127.0.0.1/qqfenzu/s/%E6%83%85%E4%BE%A3" -Tc 5 -Tw 2 -Soc 70000 -OUTMSGPRE "browser-search-qqfengzu"
#task name:browser-search-qqfengzu
check_http  -H www.gexing.com -I 123.103.21.144 -u "/qqfenzu/s/%E6%83%85%E4%BE%A3" -c 5 -w 2 --pagesize=70000:1024000

#qq皮肤搜索接口:
#php ./checkCurlHttp.php -H www.gexing.com -U "http://127.0.0.1/qqpifu/s/%E7%A4%BE%E4%BC%9A" -Tc 5 -Tw 2 -Soc 35000 -OUTMSGPRE "browser-search-qqpifu"
#task name: browser-search-qqpifu
check_http  -H www.gexing.com -I 123.103.21.144 -u "/qqpifu/s/%E7%A4%BE%E4%BC%9A" -c 5 -w 2 --pagesize=35000:1024000
#空间皮肤搜索接口：
#php ./checkCurlHttp.php -H www.gexing.com -U "http://127.0.0.1/pifu/s/%E5%B0%8F%E6%B8%85%E6%96%B0" -Tc 5 -Tw 2 -Soc 50000  -OUTMSGPRE "browser-search-kongjianpifu"
#task name:browser-search-kongjianpifu
check_http  -H www.gexing.com -I 123.103.21.144 -u "/pifu/s/%E5%B0%8F%E6%B8%85%E6%96%B0" -c 5 -w 2 --pagesize=50000:1024000

#壁纸搜索接口：
#php ./checkCurlHttp.php -H www.gexing.com -U "http://127.0.0.1/bizhi/s/%E9%A3%8E%E6%99%AF" -Tc 5 -Tw 2 -Soc 50000 -OUTMSGPRE "browser-search-bizhi"
#task name:browser-search-bizhi
check_http  -H www.gexing.com -I 123.103.21.144 -u "/bizhi/s/%E9%A3%8E%E6%99%AF" -c 5 -w 2 --pagesize=50000:1024000





















#!/bin/sh
#浏览器请求接口监控－sso

#1.通行证登录接口：注意sso.gexing.com的ip地址:此接口部署到前端机即可
#php ./checkCurlHttp.php -U "http://sso.gexing.com/index.php?action=login&callback=jQuery172011129305587379841_1364190922026&email=sqj0213@163.com&password=asdfasdf&successUri=http://www.gexing.com/&dataType=json&remember=1&_=1364281767632"  -CKW  -Tc 5 -Tw 2 -G "ok" -OBF /tmp/login.content -OUTMSGPRE "browser-sso-xhr-login" -OUTFORMAT json 1>/tmp/checkSso.log 2>/tmp/checkSso.log.2
#task name:browser-sso-xhr-login
check_http  -H sso.gexing.com -I 123.103.21.144 -u "/index.php?action=login&callback=jQuery172011129305587379841_1364190922026&email=sqj0213@163.com&password=asdfasdf&successUri=http://www.gexing.com/&dataType=json&remember=1&_=1364281767632" --string="ok" -c 5 -w 2 

# 脚本返回:
#Page OK: HTTP Status Code 200 - 795 bytes in 1.404606 seconds |time=1.405 size=795
#2.登录成功后的web登录同步接口并setcookie:
#php ./checkCurlHttp.php -U /tmp/login.content  -CKW  -Tc 5 -Tw 2 -G "ok" -OUTMSGPRE "browser-sso-synclogin-setcookie" -OUTFORMAT json 1>>/tmp/checkSso.log 2>>/tmp/checkSso.log.2
#task name: browser-www-xhr-synclogin-setcookie

check_http  -H www.gexing.com -I 172.16.3.5 -u "/index.php?action=sync_login&info=de64QCYH5P0n6p3J1iMIWxEQZsk6xg8E9r03jKKjDTbHOBphtDgxNjNR4PaCDKyLFW8l%2BaoQMuVEa5n5RkhRi5mviH1ybCCYf%2B5QZcG9b90oCmn0pYnoy%2ByvTvYJVJRj8Jh%2By4F%2Bfu4DS7iW3EMX5cu2EFDMoLh%2Fzq2Ist19pwbnkFDWyClhZ8%2BFmSyV9Xswx%2FOx1HFW5HBol7ubY2HMBAegc%2F5%2F5GJuOaE3jWPuDbY5saImhSGmkj2Gag3NMP46bIiNbYIpkU62lkMdUxjZxuam8p5%2BTKIu8R6Z%2BxewUWLvKHv%2FKzN2lvoI%2FbJBnpsTFsgFJZvW20Dn9%2FDCDAfd4MwvuoOC%2FqkFb0yARXa61mlZlrnKuZBU2fkwF4%2BOd7hlMMoYWC4hQb91Hg2Tx7vwa9UpgyefZynPBfebKpI8jX%2FhEu2n900Z1TM%2BgHBNzA5FJ7RKOs1VL9W9Vn%2Bo8MTeNS2cYQS92tMB3W2bOQxDYQmtV6jHOEtS8f8U55HCqa8l5bCin%2BXpYu54kQ&verify=aef3480f1170676ee500cd455497a716" -c 5 -w 2 
#3.判断用户是否登录的js接口:
#task name: browser-www-xhr-ajax_getLoginStatus
#php ./checkCurlHttp.php -U "http://www.gexing.com/api/index.php?callback=jQuery1720655312596072878_1364200740688&action=ajax_getLoginStatus&_=1364200741270" -G "6336831" -CKR -Tc 5 -Tw 2 -OUTMSGPRE "browser-sso-xhr-ajax_getLoginStatus"  -OUTFORMAT json 1>>/tmp/checkSso.log 2>>/tmp/checkSso.log.2
check_http  -H www.gexing.com -I 172.16.3.5 -u "/api/index.php?callback=jQuery1720655312596072878_1364200740688&action=ajax_getLoginStatus&_=1364200741270" -c 5 -w 2 --string="6336831" --header="Cookie: al=89ccomXcC2lg50OWFyTQmaNIiDu0l31ZvsxE%2Fp3HxLtmRC9X6%2ByUZEY3mFeB3DtOdjp1aej8ybAna8hWl9G4EgBh17RuRQvILNqCKXTV" --header="Cookie: us=803e6d4IDr%2F8LI%2Fi9XrsnYVCpY0whh65OFu%2BEpbYQG%2Brnlqj6z%2FlHIPZB3%2F4zwP8rbhAPWXMHWMTSRoDP2M12tZrgjZEvHamopzqW7IIXiKA7qQMDa%2BMs2hpk8t49hj8%2FfDiqqvHUqu8lUMIZi5qxV7H2zeSvr72lbxHZA"
#4.取用户登录信息接口直接返回js:
#php ./checkCurlHttp.php -U "http://www.gexing.com/api/index.php?callback=jQuery1720655312596072878_1364200740689&action=indexTopLginjs&_=1364200741597" -G "6336831" -CKR  -Tc 5 -Tw 2 -OUTMSGPRE "browser-sso-xhr-indexTopLginjs"  -OUTFORMAT json 1>>/tmp/checkSso.log 2>>/tmp/checkSso.log.2
#task name: browser-www-xhr-indexTopLginjs
check_http  -H www.gexing.com -I 172.16.3.5 -u "/api/index.php?callback=jQuery1720655312596072878_1364200740689&action=indexTopLginjs&_=1364200741597"" -c 5 -w 2 --string="6336831" --header="Cookie: al=89ccomXcC2lg50OWFyTQmaNIiDu0l31ZvsxE%2Fp3HxLtmRC9X6%2ByUZEY3mFeB3DtOdjp1aej8ybAna8hWl9G4EgBh17RuRQvILNqCKXTV" --header="Cookie: us=803e6d4IDr%2F8LI%2Fi9XrsnYVCpY0whh65OFu%2BEpbYQG%2Brnlqj6z%2FlHIPZB3%2F4zwP8rbhAPWXMHWMTSRoDP2M12tZrgjZEvHamopzqW7IIXiKA7qQMDa%2BMs2hpk8t49hj8%2FfDiqqvHUqu8lUMIZi5qxV7H2zeSvr72lbxHZA"
