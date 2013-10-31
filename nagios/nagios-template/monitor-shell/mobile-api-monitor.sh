#!/bin/sh

#手机接口监控:
#    1.登录接口
#	http://sso.gexing.com/?action=login&email=sqj0213@163.com&password=asdfasdf&application=android&dataType=json
#task name: mobile-api-sso
check_http  -H sso.gexing.com -I 123.103.21.144 -u "/?action=login&email=sqj0213@163.com&password=asdfasdf&application=android&dataType=json" --string="6336831" -c 5 -w 2

#    1.会话详情
#        http://shouji.gexing.com/z/?abaca_module=mood&abaca_action=api_dialogue_info&id=4837519&Pid=&type=mood&Chat_type=&size=5
#task name: mobile-mood-api_dialogue_info

check_http  -H shouji.gexing.com -I 60.2.235.71 -u "/z/?abaca_module=mood&abaca_action=api_dialogue_info&id=4837519&Pid=&type=mood&Chat_type=&size=5"  --header="Cookie: al=89ccomXcC2lg50OWFyTQmaNIiDu0l31ZvsxE%2Fp3HxLtmRC9X6%2ByUZEY3mFeB3DtOdjp1aej8ybAna8hWl9G4EgBh17RuRQvILNqCKXTV" --header="Cookie: us=803e6d4IDr%2F8LI%2Fi9XrsnYVCpY0whh65OFu%2BEpbYQG%2Brnlqj6z%2FlHIPZB3%2F4zwP8rbhAPWXMHWMTSRoDP2M12tZrgjZEvHamopzqW7IIXiKA7qQMDa%2BMs2hpk8t49hj8%2FfDiqqvHUqu8lUMIZi5qxV7H2zeSvr72lbxHZA" --string="4837519" -c 5 -w 2

#    2.发起新会话
#        http://shouji.gexing.com/z/?abaca_module=mood&abaca_action=api_publish_mood&content=%E6%96%B0%E5%B9%B4%E5%A5%BD%E4%B8%87%E4%BA%8B%E5%A6%82%E6%84%8F&images=[]
#task name: mobile-mood-api_publish_mood
check_http  -H shouji.gexing.com -I 60.2.235.71 -u "/z/?abaca_module=mood&abaca_action=api_publish_mood&content=%E6%96%B0%E5%B9%B4%E5%A5%BD%E4%B8%87%E4%BA%8B%E5%A6%82%E6%84%8F&images=[]"  --header="Cookie: al=89ccomXcC2lg50OWFyTQmaNIiDu0l31ZvsxE%2Fp3HxLtmRC9X6%2ByUZEY3mFeB3DtOdjp1aej8ybAna8hWl9G4EgBh17RuRQvILNqCKXTV" --header="Cookie: us=803e6d4IDr%2F8LI%2Fi9XrsnYVCpY0whh65OFu%2BEpbYQG%2Brnlqj6z%2FlHIPZB3%2F4zwP8rbhAPWXMHWMTSRoDP2M12tZrgjZEvHamopzqW7IIXiKA7qQMDa%2BMs2hpk8t49hj8%2FfDiqqvHUqu8lUMIZi5qxV7H2zeSvr72lbxHZA" --string="E0000000" -c 5 -w 2

#    3.相册详情
#        http://shouji.gexing.com/z/?abaca_action=api_albumpic&abaca_module=album&uid=6336831&albumId=26 E0000000
#task name: mobile-album-api_albumpic
check_http  -H shouji.gexing.com -I 60.2.235.71 -u "/z/?abaca_action=api_albumpic&abaca_module=album&uid=6336831&albumId=26"  --header="Cookie: al=89ccomXcC2lg50OWFyTQmaNIiDu0l31ZvsxE%2Fp3HxLtmRC9X6%2ByUZEY3mFeB3DtOdjp1aej8ybAna8hWl9G4EgBh17RuRQvILNqCKXTV" --header="Cookie: us=803e6d4IDr%2F8LI%2Fi9XrsnYVCpY0whh65OFu%2BEpbYQG%2Brnlqj6z%2FlHIPZB3%2F4zwP8rbhAPWXMHWMTSRoDP2M12tZrgjZEvHamopzqW7IIXiKA7qQMDa%2BMs2hpk8t49hj8%2FfDiqqvHUqu8lUMIZi5qxV7H2zeSvr72lbxHZA" --string="E0000000" -c 5 -w 2

#    4.相册列表
#        http://shouji.gexing.com/z/?abaca_action=api_list&abaca_module=album
#task name: mobile-album-api_list
check_http  -H shouji.gexing.com -I 60.2.235.71 -u "/z/?abaca_action=api_list&abaca_module=album&uid=6336831&albumId=2"  --header="Cookie: al=89ccomXcC2lg50OWFyTQmaNIiDu0l31ZvsxE%2Fp3HxLtmRC9X6%2ByUZEY3mFeB3DtOdjp1aej8ybAna8hWl9G4EgBh17RuRQvILNqCKXTV" --header="Cookie: us=803e6d4IDr%2F8LI%2Fi9XrsnYVCpY0whh65OFu%2BEpbYQG%2Brnlqj6z%2FlHIPZB3%2F4zwP8rbhAPWXMHWMTSRoDP2M12tZrgjZEvHamopzqW7IIXiKA7qQMDa%2BMs2hpk8t49hj8%2FfDiqqvHUqu8lUMIZi5qxV7H2zeSvr72lbxHZA" --string="E0000000" -c 5 -w 2

#    5.关系圈列表详情接口
#        http://shouji.gexing.com/z/?abaca_action=api_get_members&abaca_module=friend&circle_id=1&uid=6336831
#task name :mobile-friend-api_get_members
check_http  -H shouji.gexing.com -I 60.2.235.71 -u "/z/?abaca_action=api_get_members&abaca_module=friend&circle_id=1&uid=6336831"  --header="Cookie: al=89ccomXcC2lg50OWFyTQmaNIiDu0l31ZvsxE%2Fp3HxLtmRC9X6%2ByUZEY3mFeB3DtOdjp1aej8ybAna8hWl9G4EgBh17RuRQvILNqCKXTV" --header="Cookie: us=803e6d4IDr%2F8LI%2Fi9XrsnYVCpY0whh65OFu%2BEpbYQG%2Brnlqj6z%2FlHIPZB3%2F4zwP8rbhAPWXMHWMTSRoDP2M12tZrgjZEvHamopzqW7IIXiKA7qQMDa%2BMs2hpk8t49hj8%2FfDiqqvHUqu8lUMIZi5qxV7H2zeSvr72lbxHZA" --string="E0000000" -c 5 -w 2

#    6.用户资料接口
#        http://shouji.gexing.com/z/?abaca_action=user_list&abaca_module=user
#task name: mobile-user-user_list
check_http  -H shouji.gexing.com -I 60.2.235.71 -u "/z/?abaca_action=user_list&abaca_module=user"  --header="Cookie: al=89ccomXcC2lg50OWFyTQmaNIiDu0l31ZvsxE%2Fp3HxLtmRC9X6%2ByUZEY3mFeB3DtOdjp1aej8ybAna8hWl9G4EgBh17RuRQvILNqCKXTV" --header="Cookie: us=803e6d4IDr%2F8LI%2Fi9XrsnYVCpY0whh65OFu%2BEpbYQG%2Brnlqj6z%2FlHIPZB3%2F4zwP8rbhAPWXMHWMTSRoDP2M12tZrgjZEvHamopzqW7IIXiKA7qQMDa%2BMs2hpk8t49hj8%2FfDiqqvHUqu8lUMIZi5qxV7H2zeSvr72lbxHZA" --string="E0000000" -c 5 -w 2
