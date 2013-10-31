<?php
//appInc.php头必须定义如下内容
#产品引用时必须定义，不定义不可使用
define( "GEXING_SYSLOG_PRODUCT", "gexingweb" );
//非必定义
define( "GEXING_SYSLOG_MODULE", "BBS" );

//调试,file_put_contents输出，请千万小心
define( "GEXING_SYSLOG_DEBUG_FLAG", false );
define( "GEXING_SYSLOG_DEBUG_FILE_PATH", "/var/log/GEXINGDebug.log" );



require_once( "./GEXINGSyslog.php" );

//单条日志调用形式，如果同一文件有多处写日志请求，请不要使用此函数
//文件名与行号:日志无file与line键值，系统自动补全，补全方式为doLog函数被调用时所在的文件名与行号。建议记日志处加file与line两键
//module键:GEXING_SYSLOG_MODULE已经定义,系统自动补入msg里

$level = LOG_INFO_STORE;
$data = array( 
			'summary'=>"update data",
			'detail'=>"update data info:update data succes"
			);
GEXINGSyslog::doLog( $level, $data );

//module键:自定义写日志方式
$level = LOG_INFO_STORE;
$data = array( 
			'module'=>'blog',
			'summary'=>"update data",
			'detail'=>"update data info:update data succes"
			);
GEXINGSyslog::doLog( $level, $data );

//文件名与行号:应用自己写的方式
$level = LOG_INFO_STORE;
$data = array( 
			'module'=>'blog',
			'summary'=>"update data",
			'detail'=>"update data info:update data succes",
			'file'=>__FILE__,
			'line'=>__LINE__
			);
GEXINGSyslog::doLog( $level, $data );


$level = LOG_INFO_STORE;
//注意:多条日志形式的file与line强烈建议应用自己去获取，否则所有日志的行号都相同
//多条日志调用形式，如果同一文件有多处写日志请求，请使用此函数
//文件名与行号:建议每条日志都要包含file与line，系统自动补全补全方式为doLog函数被调用时所在的文件名与行号，导致所有行号相同
//module键:无module键，module键以GEXING_SYSLOG_MODULE宏值填充，若GEXING_SYSLOG_MODULE未定义，module键以GEXING_SYSLOG_PRODUCT宏值填充
$data = array( 
			0=>array(
					'summary'=>"update data0",
					'detail'=>"update data0 succes"
					),
			1=>array(

					'summary'=>"update data1",
					'detail'=>"update data1 failed:connect db error!"
					)
			);
GEXINGSyslog::doLog( $level, $data );
?>