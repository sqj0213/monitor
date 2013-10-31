<?php
define("DEBUG",False);

#define("ISWEB",False);
if (isset( $_GET['isstorage'] ))
{
define("NGINX_ACCESS_LOG_PATH_TMPL", "/data/site_log/storage/nginx/_DATE_/_H_-_DOMAIN_-access.log");
define("NGINX_ERROR_LOG_PATH_TMPL", "/data/site_log/storage/nginx/_DATE_/_H_-_DOMAIN_-error.log");
define("MESSAGE_LOG_PATH_TMPL", "/data/site_log/storage/messages/_DATE_/_H_-messages");
define("PHPERROR_LOG_PATH_TMPL", "/data/site_log/storage/php-fpm/_DATE_/_H_-php-fpm-error.log");
define("PHPWWWERROR_LOG_PATH_TMPL", "/data/site_log/storage/php-fpm/_DATE_/_H_-php-fpm-www-error.log");
define("PHPSLOW_LOG_PATH_TMPL", "/data/site_log/storage/php-fpm/_DATE_/_HOST_-php-fpm-slow.log");
}
else
{
define("NGINX_ACCESS_LOG_PATH_TMPL", "/data/site_log/webFront/nginx/_DATE_/_H_-_DOMAIN_-access.log");
define("NGINX_ERROR_LOG_PATH_TMPL", "/data/site_log/webFront/nginx/_DATE_/_H_-_DOMAIN_-error.log");
define("MESSAGE_LOG_PATH_TMPL", "/data/site_log/webFront/messages/_DATE_/_H_-messages");
define("PHPERROR_LOG_PATH_TMPL", "/data/site_log/webFront/php-fpm/_DATE_/_H_-php-fpm-error.log");
define("PHPWWWERROR_LOG_PATH_TMPL", "/data/site_log/webFront/php-fpm/_DATE_/_H_-php-fpm-www-error.log");
define("PHPSLOW_LOG_PATH_TMPL", "/data/site_log/webFront/php-fpm/_DATE_/_HOST_-php-fpm-slow.log");
}

$fatalErrorCount = 0;
$warningErrorCount = 0;
$noticeErrorCount = 0;
$parseErrorCount = 0;



function help( $argv )
{
	global $domain;
	global $interval;
	global $time;

	if ( Empty( $domain ) || Empty( $interval ) || Empty($time ) )
	{

		if ( isset( $_GET )  )
		{
			echo "time:".$time."\tdomain:".$domain."\thostName:".$hostName."\tinterval:".$interval."<br><br>";
			echo "read log help:<br><br>";
			echo "\t\tphp ./readLog.php \"2013-04-05 16:54:55\" 500 sso.gexing.com [picses-bj17] [/var/log/message]<br><br>";
			echo "http://ip:port/webFront/readLog.php?time=2013-04-05 16:54:55&interval=500&domain=sso.gexing.com&hostName=<br><br>";
			echo "<br><br>";
		}
		else
		{
			echo "time:".$time."\tdomain:".$domain."\thostName:".$hostName."\tinterval:".$interval."\n\n";
			echo "read log help:\n\n";
			echo "\t\tphp ./readLog.php \"2013-04-05 16:54:55\" 500 sso.gexing.com [picses-bj17] [/var/log/message]\n\n";
			echo "http://ip:port/webFront/readLog.php?time=2013-04-05 16:54:55&interval=500&domain=sso.gexing.com&hostName=\n\n";
			echo "\n\n";
		}
		exit;
	}
}

if ( isset( $_GET['time'] ) )
{
	$dateTimeObj = new DateTime($_GET['time']);
	$currentDateTime=$dateTimeObj->format("Y-m-d H:i:s");
	$currentDate=$dateTimeObj->format("Y-m-d");
	$currentHour = $dateTimeObj->format("H");

	define("ISWEB",True);
	$time = $_GET['time'];

	$interval = $_GET['interval'];
	$domain = $_GET['domain'];

	$hostName = isset($_GET['hostName'])?$_GET['hostname']:'';
	echo "time:".$time."\tdomain:".$domain."\thostName:".$hostName."\tinterval:".$interval."<br><br>";
}
else
{
	$dateTimeObj = new DateTime($argv[1]);
	$currentDateTime=$dateTimeObj->format("Y-m-d H:i:s");
	$currentDate=$dateTimeObj->format("Y-m-d");
	$currentHour = $dateTimeObj->format("H");

	define("ISWEB",False);
	$time = $argv[1];
	$interval = $argv[2];
	$domain = isset($argv[3])? $argv[3]:"";
	$hostName = isset( $argv[4] ) ? $argv[4]:"";
	echo "time:".$time."\tdomain:".$domain."\thostName:".$hostName."\tinterval:".$interval."\n\n";

}
help(isset($argv)?$argv:$_GET);


function readFileList( $dir, $keyStr="")
{
	$retData = array();
	$dirHandler = opendir( $dir );
	if ( $dirHandler )
	{
		while ( ( $file = readdir($dirHandler) ) !== false )
		{
			if ( strpos( $file, $keyStr ) !== false )
				array_push( $retData, $file );
		}
	}
	return $retData;
}
function readPhpSlowLogMain($dateTime, $currentDate, $currentHour, $interval, $hostName="")
{
	echo "<font color=green><b>--------------------PHP-FPM-SLOW  LOG(begin!)---------------------</b></font><br><br>";

	$msgBody = "";
	$dateTimeInt = $dateTime->getTimestamp();
	$logPath = str_replace("_DATE_", $currentDate, PHPSLOW_LOG_PATH_TMPL );
	$logPath = str_replace("_H_", "" ,$logPath);
	$logPath = str_replace("_HOST_-", "", $logPath);
	$fileKeyStr = substr( $logPath, strrpos( $logPath, "/")+1 );
	$phpSlowLogDir = dirname( $logPath );
	$fileList = readFileList( $phpSlowLogDir, $fileKeyStr );
	while ( current( $fileList ) !== false )
	{
		$hostName1 = substr(current($fileList), 0, strpos(current($fileList),"-php"));
		if ( !Empty( $hostName ) )
		{
			if ( $hostName == $hostName1 )
				$bodyStr = readPhpSlowLog( $dateTime, $currentDate, $currentHour, $interval,$hostName1 );
		}
		else
			$bodyStr = readPhpSlowLog( $dateTime, $currentDate, $currentHour, $interval,$hostName1 );
		if ( ISWEB )
			echo str_replace(  PHP_EOL, "<br>", $bodyStr );
		else
			echo $bodyStr;
		next( $fileList);
	}
	echo "<font color=green><b>--------------------PHP-FPM-SLOW  LOG(end!)---------------------</b></font><br><br>";
}

function readNginxAccessLog( $dateTime, $currentDate, $currentHour, $interval,$domain="sso.gexing.com", $hostName="" )
{
	$nginxLogTitle = "<font color=green><b>--------------------_DOMAIN_ NGINX ACCESS LOG(begin!)---------------------</b></font>\n\n";
	$msgBody = "";
	$dateTimeInt = $dateTime->getTimestamp();
	$logPath = str_replace("_DATE_", $currentDate, NGINX_ACCESS_LOG_PATH_TMPL );
	$logPath = str_replace("_H_", $currentHour,$logPath);
	$logPath = str_replace("_DOMAIN_", $domain,$logPath);
	$fileHandler = fopen( $logPath, "r");
	while( $line = fgets($fileHandler) )
	{
		$tmp1 =  explode("  ", $line );
		if ( !Empty( $hostName ) && $tmp1[0] == $hostName )
		{
			$lineTime = strtotime($tmp1[2]);
			if ( abs($lineTime-$dateTimeInt) <= $interval )
			{
				if ( $tmp1[8] != "rc:200" and  $tmp1[8] != "rc:302" )
				{
					$line = str_replace("rc:400", "<font color=red><b>rc:400</b></font>", $line);
					$line = str_replace("rc:500", "<font color=red><b>rc:500</b></font>", $line);
					$line = str_replace("rc:502", "<font color=red><b>rc:502</b></font>", $line);

					$msgBody .= $line;
					if ( DEBUG )
					{
						echo "$tmp1[2]:$lineTime:".strftime("%Y-%m-%d %H:%M:%S", $lineTime)."\n\n";
						echo $line;
					}
				}
			}

		}
		if ( Empty( $hostName ) )
		{
			$lineTime = strtotime($tmp1[2]);
			if ( abs($lineTime-$dateTimeInt) <= $interval )
			{
				if ( $tmp1[8] != "rc:200" and  $tmp1[8] != "rc:302" )
				{
					$line = str_replace("rc:400", "<font color=red><b>rc:400</b></font>", $line);
					$line = str_replace("rc:500", "<font color=red><b>rc:500</b></font>", $line);
					$line = str_replace("rc:502", "<font color=red><b>rc:502</b></font>", $line);
					$msgBody .= $line;
					if ( DEBUG )
					{
						echo "$tmp1[2]:$lineTime:".strftime("%Y-%m-%d %H:%M:%S", $lineTime)."\n\n";
						echo $line;
					}
				}
			}
		}
	}
	return str_replace("_DOMAIN_", $domain, $nginxLogTitle.$msgBody."<font color=green><b>--------------------_DOMAIN_ NGINX ACCESS LOG(end!)---------------------</b></font>\n\n");
}

function readNginxErrorLog( $dateTime, $currentDate, $currentHour, $interval, $domain="sso.gexing.com", $hostName="" )
{
	global $warningErrorCount;
	global $noticeErrorCount;
	$nginxLogTitle = "<font color=green><b>--------------------_DOMAIN_ NGINX ERROR LOG(begin!)---------------------</b></font>\n\n";
	$msgBody = "";
	$dateTimeInt = $dateTime->getTimestamp();
	$logPath = str_replace("_DATE_", $currentDate, NGINX_ERROR_LOG_PATH_TMPL );
	$logPath = str_replace("_H_", $currentHour,$logPath);
	$logPath = str_replace("_DOMAIN_", $domain,$logPath);
	$fileHandler = fopen( $logPath, "r");
	while( $line = fgets($fileHandler) )
	{
		if ( strpos( $line, "No such file or directory" )=== false )
		{
			$lineTime = strtotime(substr( $line, strpos( $line, "   " ) + 3, 19 ));
			if ( !Empty( $hostName ) && $hostName == substr( $line, strpos( $line, " " ) ) )
			{
				if ( abs($lineTime-$dateTimeInt) <= $interval )
				{
					if ( strpos( $line, "PHP Warning" ) !== false )
					{
						$warningErrorCount++;
						$line = str_replace("PHP Warning", "<font color=blue><b>PHP Warning</b></b></font>", $line);
					}
					elseif ( strpos( $line, "PHP Notice" ) !== false )
					{
						$noticeErrorCount++;
					}
					$msgBody .= $line;
					if ( DEBUG )
					{
						echo "$lineTime:".strftime("%Y-%m-%d %H:%M:%S", $lineTime)."\n\n";
						echo $line;
					}
				}
			}
			if ( Empty( $hostName ) )
			{
				if ( abs($lineTime-$dateTimeInt) <= $interval )
				{
					if ( strpos( $line, "PHP Warning" ) !== false )
					{
						$warningErrorCount++;
						$line = str_replace("PHP Warning", "<font color=blue><b>PHP Warning</b></b></font>", $line);
					}
					elseif ( strpos( $line, "PHP Notice" ) !== false )
					{
						$noticeErrorCount++;
					}
					$msgBody .= $line;
					if ( DEBUG )
					{
						echo "$lineTime:".strftime("%Y-%m-%d %H:%M:%S", $lineTime)."\n\n";
						echo $line;
					}
				}
			}
		}
	}
	return str_replace("_DOMAIN_", $domain, $nginxLogTitle.$msgBody."<font color=green><b>--------------------_DOMAIN_ NGINX ERROR LOG(end!)---------------------</b></font>\n\n");
}
function readMessagesLog( $dateTime, $currentDate, $currentHour, $interval,$hostName="" )
{
	$nginxLogTitle = "<font color=green><b>--------------------webFront messages log (begin!)---------------------</b></font>\n\n";
	$msgBody = "";
	$dateTimeInt = $dateTime->getTimestamp();
	$logPath = str_replace("_DATE_", $currentDate, MESSAGE_LOG_PATH_TMPL );
	$logPath = str_replace("_H_", $currentHour,$logPath);
	if ( file_exists( $logPath ) )
	{
		$fileHandler = fopen( $logPath, "r");
		while( $line = fgets($fileHandler) )
		{
			$lineTime = strtotime(substr( $line, strpos( $line, "   " ) + 3, 15 ));

			if ( !Empty( $hostName ) && $hostName == substr( $line, strpos( $line, " " ) ) )
			{

				if ( abs($lineTime-$dateTimeInt) <= $interval )
				{
					$msgBody .= $line;
					if ( DEBUG )
					{
						echo "$tmp1[2]:$lineTime:".strftime("%Y-%m-%d %H:%M:%S", $lineTime)."\n\n";
						echo $line;
					}
				}
			}
			if ( Empty( $hostName ) )

			{
				if ( abs($lineTime-$dateTimeInt) <= $interval )
				{
					$msgBody .= $line;
					if ( DEBUG )
					{
						echo "$tmp1[2]:$lineTime:".strftime("%Y-%m-%d %H:%M:%S", $lineTime)."\n\n";
						echo $line;
					}
				}


			}
		}
	}
	return $nginxLogTitle.$msgBody."<font color=green><b>--------------------webFront messages log (end!)---------------------</b></font>\n\n";
}
function readPhpErrorLog( $dateTime, $currentDate, $currentHour, $interval,$hostName="" )
{
	$nginxLogTitle = "<font color=green><b>--------------------PHP-FPM-ERROR LOG(begin!)---------------------</b></font>\n\n";
	$msgBody = "";
	$dateTimeInt = $dateTime->getTimestamp();
	$logPath = str_replace("_DATE_", $currentDate, PHPERROR_LOG_PATH_TMPL );
	$logPath = str_replace("_H_", $currentHour,$logPath);
	$fileHandler = fopen( $logPath, "r");
	while( $line = fgets($fileHandler) )
	{
		$lineTime = strtotime(substr( $line, strpos( $line, "[" ) + 1, 20 ));
		if ( !Empty( $hostName ) && $hostName == substr( $line, strpos( $line, " " ) ) )
		{
			if ( abs($lineTime-$dateTimeInt) <= $interval )
			{
				$msgBody .= $line;
				if ( DEBUG )
				{
					echo "$lineTime:".strftime("%Y-%m-%d %H:%M:%S", $lineTime)."\n\n";
					echo $line;
				}
			}
		}

		if ( Empty( $hostName ) )
		{
			if ( abs($lineTime-$dateTimeInt) <= $interval )
			{
				$msgBody .= $line;
				if ( DEBUG )
				{
					echo "$lineTime:".strftime("%Y-%m-%d %H:%M:%S", $lineTime)."\n\n";
					echo $line;
				}
			}
		}
	}
	return $nginxLogTitle.$msgBody."<font color=green><b>--------------------PHP-FPM-ERROR LOG(end!)---------------------</b></font>\n\n";
}

function readPhpWWWErrorLog( $dateTime, $currentDate, $currentHour, $interval,$hostName="",$timezoneDiff=28800 )
{
	global $fatalErrorCount;
	global $parseErrorCount;
	$nginxLogTitle = "<font color=green><b>--------------------PHP-FPM-WWW-ERROR LOG(begin!)---------------------</b></font>\n\n";
	$msgBody = "";
	$dateTimeInt = $dateTime->getTimestamp();
	$logPath = str_replace("_DATE_", $currentDate, PHPWWWERROR_LOG_PATH_TMPL );
	$logPath = str_replace("_H_", $currentHour,$logPath);
	$fileHandler = fopen( $logPath, "r");
	while( $line = fgets($fileHandler) )
	{
		$lineTime = strtotime(substr( $line, strpos( $line, "[" ) + 1, 20 ))+$timezoneDiff;
		if ( !Empty( $hostName ) && $hostName == substr( $line, strpos( $line, " " ) ) )
		{
			if ( abs($lineTime-$dateTimeInt) <= $interval )
			{
				if ( strpos( $line, "PHP Warning" ) !== false )
				{
					$line = str_replace("PHP Warning", "<font color=blue><b>PHP Warning</b></b></font>", $line);
				}
				elseif ( strpos( $line, "PHP Fatal error" ) !== false )
				{
					$fatalErrorCount++;
					$line = str_replace("PHP Fatal error", "<font color=red><b>PHP Fatal error</b></b></font>", $line);
				}
				elseif ( strpos( $line, "PHP Parse error" ) !== false )
				{
					$parseErrorCount++;
					$line = str_replace("PHP Parse error", "<font color=red><b>PHP Parse error</b></b></font>", $line);
				}


				$msgBody .= $line;
				if ( DEBUG )
				{
					echo "$lineTime:".strftime("%Y-%m-%d %H:%M:%S", $lineTime)."\n\n";
					echo $line;
				}
			}
		}
		if ( Empty( $hostName ) )
		{
			if ( abs($lineTime-$dateTimeInt) <= $interval )
			{
				if ( strpos( $line, "PHP Warning" ) !== false )
				{
					$warningErrorCount++;
					$line = str_replace("PHP Warning", "<font color=blue><b>PHP Warning</b></b></font>", $line);
				}
				elseif ( strpos( $line, "PHP Fatal error" ) !== false )
				{
					$fatalErrorCount++;
					$line = str_replace("PHP Fatal error", "<font color=red><b>PHP Fatal error</b></b></font>", $line);
				}
				elseif ( strpos( $line, "PHP Parse error" ) !== false )
				{
					$parseErrorCount++;
					$line = str_replace("PHP Parse error", "<font color=red><b>PHP Parse error</b></b></font>", $line);
				}


				$msgBody .= $line;
				if ( DEBUG )
				{
					echo "$lineTime:".strftime("%Y-%m-%d %H:%M:%S", $lineTime)."\n\n";
					echo $line;
				}
			}
		}
	}
	return $nginxLogTitle.$msgBody."<font color=green><b>--------------------PHP-FPM-WWW-ERROR LOG(end!)---------------------</b></font>\n\n";
}







function readPhpSlowLog( $dateTime, $currentDate, $currentHour, $interval,$hostName="" )
{
	$nginxLogTitle = "<font color=green><b>--------------------_HOST_ PHP-FPM-SLOW LOG(begin!)---------------------</b></font>\n\n";
	$msgBody = "";
	$dateTimeInt = $dateTime->getTimestamp();
	$logPath = str_replace("_DATE_", $currentDate, PHPSLOW_LOG_PATH_TMPL);
	$logPath = str_replace("_H_", "",$logPath);
	$logPath = str_replace("_HOST_", $hostName ,$logPath);
	$fileHandler = fopen( $logPath, "r");
	while( $line = fgets($fileHandler) )
	{
		/*
		 pisces-bj17   [07-Apr-2013 10:15:22]  [pool www] pid 4788
		pisces-bj17   script_filename = /data/www/htdocs/mobile.gexing.com/v1.1/list.qianming.php
		pisces-bj17   [0x00007f90a4631c58] fread() /data/www/htdocs/www.gexing.com/abaca/class/SphinxClient.class.php:627
		pisces-bj17   [0x00007f90a4631680] _GetResponse() /data/www/htdocs/www.gexing.com/abaca/class/SphinxClient.class.php:1113
		pisces-bj17   [0x00007f90a46312e8] RunQueries() /data/www/htdocs/www.gexing.com/abaca/class/SphinxClient.class.php:952
		pisces-bj17   [0x00007f90a46300a0] Query() /data/www/htdocs/www.gexing.com/abaca/class/Post.class.php:1035
		pisces-bj17   [0x00007f90a462c0c8] searchTag() /data/www/htdocs/www.gexing.com/abaca/class/Post.class.php:1312
		pisces-bj17   [0x00007f90a4629280] getSpecifiedPostIds() /data/www/htdocs/mobile.gexing.com/v1.1/list.qianming.php:60

		*/
		$timeField = substr( $line, strpos( $line, " [" ) + 2, 20);
		if ( is_numeric( substr( $timeField, 0,2  ) ) && is_numeric( substr( $timeField,-1, 2 ) ))
		{


			$startPos = ftell( $fileHandler);
			$lineCount = 0;
			$msgBodyMiddle = "";
			while ( $line1 = fgets($fileHandler))
			{
				$timeField1 = substr( $line1, strpos( $line1, " [" ) + 2, 20);
				if (is_numeric( substr( $timeField1, 0,2  ) ) && is_numeric( substr( $timeField1,-1, 2 ) ))
				{
					fseek( $fileHandler,$startPos );
					break;
				}
				else
				{
					$msgBodyMiddle .= $line1;
					$lineCount += 1;
				}
				$startPos = ftell( $fileHandler);
				if ( $lineCount > 20 )
					break;

			}
				
			$lineTime = strtotime( $timeField );

			if ( abs($lineTime-$dateTimeInt) <= $interval )
			{
				$msgBody .= $line.$msgBodyMiddle;
				if ( DEBUG )
				{
					echo "$lineTime:".strftime("%Y-%m-%d %H:%M:%S", $lineTime)."\n\n";
					echo $line;
				}
			}
		}
	}
	return str_replace("_HOST_", $hostName, $nginxLogTitle.$msgBody."<font color=green><b>--------------------_HOST_ PHP-FPM-SLOW LOG(end!)---------------------</b></font>\n\n");
}

if ( ISWEB )
{
	$htmlStr = str_replace( PHP_EOL, "<br>", readNginxAccessLog( $dateTimeObj, $currentDate, $currentHour, $interval,$domain,$hostName)) ;
	$htmlStr .= str_replace( PHP_EOL, "<br>", readNginxErrorLog( $dateTimeObj, $currentDate, $currentHour, $interval,$domain,$hostName));
	$htmlStr .= str_replace( PHP_EOL, "<br>",  readMessagesLog( $dateTimeObj, $currentDate, $currentHour, $interval,$hostName));
	$htmlStr .= str_replace( PHP_EOL, "<br>", readPhpErrorLog( $dateTimeObj, $currentDate, $currentHour, $interval,$hostName));
	$htmlStr .= str_replace( PHP_EOL, "<br>", readPhpWWWErrorLog( $dateTimeObj, $currentDate, $currentHour, $interval,$hostName));

        if ( isset($_GET['isstorage']) )
        {
            require_once './picUploadClass.php';
            $htmlStr .= str_replace( PHP_EOL, "<br>", picUploadReadLog::readPicUploadClientLog( $dateTimeObj, $currentDate, $currentHour, $interval, $hostName));
            $htmlStr .= str_replace( PHP_EOL, "<br>", picUploadReadLog::readPicUploadServerLog( $dateTimeObj, $currentDate, $currentHour, $interval, $hostName));
            $htmlStr .= str_replace( PHP_EOL, "<br>", picUploadReadLog::readGearmanWorkerAccessLog( $dateTimeObj, $currentDate, $currentHour, $interval, $hostName));
            $htmlStr .= str_replace( PHP_EOL, "<br>", picUploadReadLog::readGearmanWorkerErrorLog( $dateTimeObj, $currentDate, $currentHour, $interval, $hostName));
            $htmlStr .= str_replace( PHP_EOL, "<br>", picUploadReadLog::readFDFSHTDLog( $dateTimeObj, $currentDate, $currentHour, $interval, $hostName));
            $htmlStr .= str_replace( PHP_EOL, "<br>", picUploadReadLog::readFDFSStoragedLog( $dateTimeObj, $currentDate, $currentHour, $interval, $hostName));
            $htmlStr .= str_replace( PHP_EOL, "<br>", picUploadReadLog::readFDFSTrackerdLog( $dateTimeObj, $currentDate, $currentHour, $interval, $hostName));
        }



	echo "PHP Fatal error count:&nbsp;&nbsp;<font color=red><b>".$fatalErrorCount."</b></font><br>";
	echo "php warning count:&nbsp;&nbsp;<font color=red><b>".$warningErrorCount."</b></font><br>";
	echo "php notice count:&nbsp;&nbsp;<font color=red><b>".$noticeErrorCount."</b></font><br>";
	echo "parse error count:&nbsp;&nbsp;<font color=red><b>".$parseErrorCount."</b></font><br>";
        
        if ( isset($_GET['isstorage']) )
        {
            require_once './picUploadClass.php';
            echo "picUploadServer error count:&nbsp;&nbsp;<font color=red><b>".$picUploadServerFatalCount."</b></font><br>";
            echo "picUploadServer error count:&nbsp;&nbsp;<font color=red><b>".$picUploadClientFatalCount."</b></font><br>";
            echo "gearmanworker slow count:&nbsp;&nbsp;<font color=red><b>".$gearmanWorkerSlowCount."</b></font><br>";
        }
	echo $htmlStr;
	echo str_replace( PHP_EOL, "<br>",  readPhpSLowLogMain($dateTimeObj, $currentDate, $currentHour, $interval, $hostName));

}
else
{
	$htmlStr = readNginxAccessLog( $dateTimeObj, $currentDate, $currentHour, $interval,$domain,$hostName);
	$htmlStr .= readNginxErrorLog( $dateTimeObj, $currentDate, $currentHour, $interval,$domain,$hostName);
	$htmlStr .= readMessagesLog( $dateTimeObj, $currentDate, $currentHour, $interval,$hostName);
	$htmlStr .= readPhpErrorLog( $dateTimeObj, $currentDate, $currentHour, $interval,$hostName);
	$htmlStr .= readPhpWWWErrorLog( $dateTimeObj, $currentDate, $currentHour, $interval,$hostName);

	echo "PHP Fatal error count:&nbsp;&nbsp;<font color=red><b>".$fatalErrorCount."</b></font><br>";
	echo "php warning count:&nbsp;&nbsp;<font color=red><b>".$warningErrorCount."</b></font><br>";
	echo "php notice count:&nbsp;&nbsp;<font color=red><b>".$noticeErrorCount."</b></font><br>";
	echo "parse error count:&nbsp;&nbsp;<font color=red><b>".$parseErrorCount."</b></font><br>";
	echo $htmlStr;
	echo readPhpSlowLogMain($dateTimeObj, $currentDate, $currentHour, $interval, $hostName);
}
?>

