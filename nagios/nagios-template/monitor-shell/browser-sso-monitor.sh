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
