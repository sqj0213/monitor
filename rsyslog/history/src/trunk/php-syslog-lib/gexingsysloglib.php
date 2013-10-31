<?php
//写日志类

define( "LOG_INFO_STORE", 0 );
//信息日志，发送给中心机进行存储
define( "LOG_WARNING_STORE", 1 );
//警告日志，发邮件给工程师同时到中心机存储，通过rsyslog实现发送邮件
define( "LOG_ERROR_STORE", 2 );
//错误日志，发送邮件与短信给相应人员，邮件以rsyslog来发送，短信通过调用可执行程序进行发送
define( "LOG_CRITICAL_STORE", 3 );
//严重错误日志，邮件与短信发送给工程师同时自动转发给系统定义的短信地址与邮件地址
define( "LOG_INFO_TEMP", 4 );
//临时日志信息，依据系统策略保存指定的时间即可自动清除
define( "LOG_WARNING_TEMP", 5 );
//临时警告信息，发送邮件给工程师,依据系统策略保存指定的时间即可自动清除
define( "LOG_ERROR_TEMP", 6 );
//错误日志，发送邮件与短信给工程师，指定时间后可自动清除




define( "GEXING_MAX_LOG_LEVEL", 6 );
define( "GEXING_MIN_LOG_LEVEL", 0 );
define( "GEXING_SYSLOG_MULTI_LOG", 2 );

//单节点最大msg为4096,系统定义为5*1024
define( "GEXING_SYSLOG_MAX_DETAIL_SIZE", 4096 );
//最大允许一次上传1000个msg
define( "GEXING_SYSLOG_MAX_DATA_ROW", 1000 );

define( "GEXING_SYSLOG_OPTION", LOG_PID );
define( "GEXING_SYSLOG_DELIMITER", "|" );
define("GEXING_DETAIL_REPLACEMENT",			'&#30;');	# 含有分割符则替换成 &#30; 控制字符record separator的HTML Entity Code，原始代码中用的是 $#30;

//错误信息代码
define( "GEXING_SYSLOG_FORMAT_VALID", 0 );
define( "GEXING_SYSLOG_PRODUCT_NOT_DEFINED", 1 );
define( "GEXING_SYSLOG_FORMAT_INVALID", 2 );
define( "GEXING_SYSLOG_LEVEL_INVALID", 3 );
define( "GEXING_SYSLOG_MSGSIZE_INVALID", 4 );
define( "GEXING_SYSLOG_DATAROW_INVALID", 5 );


//define( "GEXING_SYSLOG_DEBUG_FLAG", false );
//define( "GEXING_SYSLOG_DEBUG_FILE_PATH", "/var/log/GEXINGDebug.log" );



class GEXINGSyslog
{

	static $productList = array( 'gexingweb', 'runlog' );
	static $product = '';
	static $module = '';
	//debug可以通过msg的fiter过滤关键字来实现相应的邮件提醒与报警
	//非debug的可以直接在rsyslog里依据level配置邮件与短信提醒
	//facility的分配可以按照产品进行资源分配
	 static $priority = array(
			0=>LOG_INFO,//处理大量业务日志数据无需过滤
			1=>LOG_WARNING,//处理警告日志需要邮件提醒
			2=>LOG_ERR,//处理错误日志需要邮件与短信提醒
			3=>LOG_CRIT,//处理错误日志需要邮件与短信提醒并转发
			4=>LOG_DEBUG,//处理debug日志，短信与邮件通过filter来实现
			5=>LOG_DEBUG,//处理debug日志，短信与邮件通过filter来实现
			6=>LOG_DEBUG//处理debug日志，短信与邮件通过filter来实现
		);
	 static $facility = array(
			0=>LOG_LOCAL6,
			1=>LOG_LOCAL6,
			2=>LOG_LOCAL6,
			3=>LOG_LOCAL6,
			4=>LOG_LOCAL7,
			5=>LOG_LOCAL7,
			6=>LOG_LOCAL7
		);
	 //消息数据格式
	 static protected $fieldList = array( 'summary', 'detail','file', 'line', 'module' );
	 //最少必须包含summary,detail,file,line，可以包含module
	static $msgFieldCount = array( 4,5 );

	/**
	 * debug_backtrace 的回溯级别
	 *
	 * @var int
	 */
	static protected $trace_offset = 0;
	/**
	 * 设置 debug_backtrace 的回溯级别
	 *
	 * @param int $offset
	 */
	static public function set_trace_offset($offset)
	{
		$offset = intval($offset);
		if ($offset < 0) {
			$offset = 0;
		}
		self::$trace_offset = intval($offset);
	}

	/**
	 * 获得调用的文件名和行数
	 *
	 * @return array (0=>file, 1=>line)
	 */
	static protected function _get_called_loc() {
		$dbt = debug_backtrace();
		return array($dbt[1+self::$trace_offset]['file'], $dbt[1+self::$trace_offset]['line']);
	}


	static protected function checkData( $level, $data=array() )
	{
		if ( $level > GEXING_MAX_LOG_LEVEL || $level < GEXING_MIN_LOG_LEVEL )
			return GEXING_SYSLOG_LEVEL_INVALID;//单条日志，日志级别错误
        //若为单条日志
		if ( isset( $data[ 'detail' ] ) && isset( $data[ 'summary' ] ) && ( count( $data ) <= count( self::$fieldList ) ) )
		{

			$diffArr = array_diff( self::$fieldList, array_keys( $data ) );
			if ( !Empty( $diffArr ) && $diffArr != array( '4'=>'module' ) )
				return GEXING_SYSLOG_FORMAT_INVALID;


			if ( "" === $data[ 'detail' ]  )
				return GEXING_SYSLOG_MSGSIZE_INVALID;//msg不可以为空

			if ( strlen( $data[ 'detail' ] ) > GEXING_SYSLOG_MAX_DETAIL_SIZE )
				return GEXING_SYSLOG_MSGSIZE_INVALID;//msg过长

			return GEXING_SYSLOG_FORMAT_VALID;//单条日志形式，日志有效
		}
		//若为多条则，且超过1000行，则这回日志错误
		if ( count( $data ) > GEXING_SYSLOG_MAX_DATA_ROW )
			return GEXING_SYSLOG_DATAROW_INVALID;//日志格式错误
		return GEXING_SYSLOG_MULTI_LOG;//多条日志形式

	}
	static protected function buildMsg( $data=array() )
	{
		//若数据项未定义module,填加宏定义的module或产品宏
		if ( isset( $data[ 'module' ] ) )
		{
			if ( Empty( $data[ 'module' ] ) )
			{
				$data[ 'module' ] = self::$module;
			}
		}
		else
		{
			$data[ 'module' ] = self::$module;
		}

		//替换detail里的分割符
		$data[ 'detail' ] = str_replace( GEXING_SYSLOG_DELIMITER, GEXING_DETAIL_REPLACEMENT, $data[ 'detail' ] );

		//拼接msg
		$msg = self::$module.GEXING_SYSLOG_DELIMITER.$data[ 'summary' ].GEXING_SYSLOG_DELIMITER.$data[ 'detail' ].GEXING_SYSLOG_DELIMITER.$data['file' ].GEXING_SYSLOG_DELIMITER.$data[ 'line' ] ;
		return $msg;

	}
	static function doLog( $level, $data=array(), $selfProduct='', $selfModule='' )
	{

		
		if ( !Empty( $selfProduct ) && !Empty( $selfModule ) )
		{
			if ( in_array( $selfProduct, self::$productList ) )
			{	
				self::$product = $selfProduct;
				self::$module = $selfModule;
			}
			else
			{
				if ( defined( "GEXING_SYSLOG_DEBUG_FLAG" ) &&  GEXING_SYSLOG_DEBUG_FLAG )
					self::_GEXINGDebug( GEXING_SYSLOG_PRODUCT_NOT_DEFINED, $data );
				return GEXING_SYSLOG_PRODUCT_NOT_DEFINED;			
			}			
		}
		else
		{
			if ( !defined( 'GEXING_SYSLOG_PRODUCT' ) )
			{
				if ( defined( "GEXING_SYSLOG_DEBUG_FLAG" ) &&  GEXING_SYSLOG_DEBUG_FLAG )
					self::_GEXINGDebug( GEXING_SYSLOG_PRODUCT_NOT_DEFINED, $data );
				return GEXING_SYSLOG_PRODUCT_NOT_DEFINED;
			}

			self::$product = GEXING_SYSLOG_PRODUCT;

			if ( defined( 'GEXING_SYSLOG_MODULE' ) && "" != GEXING_SYSLOG_MODULE )
			{
				self::$module = GEXING_SYSLOG_MODULE;
			}
			else
			{
				self::$module = self::$product;
			}
		}

		//若为单条日志
		if ( isset( $data[ 'detail' ] ) )
		{
			//若未加行号调用函数进行填加
			if ( Empty( $data[ 'file' ] ) || Empty( $data[ 'line' ] ) )
			{
				list( $data[ 'file' ], $data[ 'line' ] ) = self::_get_called_loc();
			}
		}
		$checkDataResult = self::checkData( $level, $data );

		//单条日志形式写syslog
		if ( $checkDataResult === GEXING_SYSLOG_FORMAT_VALID )
		{
			openlog( self::$product, GEXING_SYSLOG_OPTION, self::$facility[ $level ] );
			syslog( self::$priority[ $level ], self::buildMsg( $data ) );
			closelog();
		}
		else if ( $checkDataResult != GEXING_SYSLOG_MULTI_LOG )
		{
			if ( defined( "GEXING_SYSLOG_DEBUG_FLAG" ) &&  GEXING_SYSLOG_DEBUG_FLAG )
				self::_GEXINGDebug( $checkDataResult, $data );
			return $checkDataResult;

		}
		//若为多条日志形式
		if ( $checkDataResult === GEXING_SYSLOG_MULTI_LOG )
		{
			$rowCount = count( $data );
			openlog( self::$product, GEXING_SYSLOG_OPTION, self::$facility[ $level ] );
			//所有日志行号相同
			$calledInfo =  self::_get_called_loc();
			for ( $i = 0;  $i < $rowCount; $i++ )
			{
				if ( isset(  $data[ $i ] ) )
				{
					$rowData = $data[ $i ];
					if ( Empty( $rowData[ 'file' ] ) || Empty( $rowData[ 'line' ] ) )
					{
						list($rowData[ 'file' ], $rowData[ 'line' ] ) = $calledInfo;
					}
					$checkDataResult = self::checkData( $level, $rowData );
					if (  $checkDataResult === GEXING_SYSLOG_FORMAT_VALID )//日志为单条日志，且级别有效则写入，否则中断
					{
						syslog( self::$priority[ $level ], self::buildMsg( $rowData ) );
					}
					else
					{
						closelog();
						if ( defined( "GEXING_SYSLOG_DEBUG_FLAG" ) &&  GEXING_SYSLOG_DEBUG_FLAG )
							self::_GEXINGDebug( $checkDataResult, $data );

						return $checkDataResult;
					}
				}
				else
				{
					closelog();
					if ( defined( "GEXING_SYSLOG_DEBUG_FLAG" ) &&  GEXING_SYSLOG_DEBUG_FLAG )
						self::_GEXINGDebug( GEXING_SYSLOG_FORMAT_INVALID, $data );
					return GEXING_SYSLOG_FORMAT_INVALID;
				}
			}
			closelog();
		}
		if ( defined( "GEXING_SYSLOG_DEBUG_FLAG" ) &&  GEXING_SYSLOG_DEBUG_FLAG )
			self::_GEXINGDebug( $checkDataResult, $data );

	}

	static protected function  _GEXINGDebug( $retCode=0, $data=array() )
	{
		$runMsg = array(
						GEXING_SYSLOG_FORMAT_VALID=>'log format is valid!',
						GEXING_SYSLOG_PRODUCT_NOT_DEFINED=>'Macro PRODUCT is not defined!',
						GEXING_SYSLOG_FORMAT_INVALID=>'log format is invalid!',
						GEXING_SYSLOG_LEVEL_INVALID=>'log level is invalid!',
						GEXING_SYSLOG_MSGSIZE_INVALID=>'log detail field size >'.GEXING_SYSLOG_MAX_DETAIL_SIZE.'!' ,
						GEXING_SYSLOG_DATAROW_INVALID=>'muti log row data >'.GEXING_SYSLOG_MAX_DATA_ROW.'!'
						);
		file_put_contents( GEXING_SYSLOG_DEBUG_FILE_PATH, 'runMsg:'.$runMsg[ $retCode ].'\tdata:'.print_r( $data, true ), FILE_APPEND );
	}
}
?>
ING_SYSLOG_DEBUG_FILE_PATH, 'runMsg:'.$runMsg[ $retCode ].'\tdata:'.print_r( $data, true ), FILE_APPEND );
	}
}
?>
