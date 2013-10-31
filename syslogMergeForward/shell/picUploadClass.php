<?php

#pic.upload全局变量
$picUploadServerFatalCount = 0;
$picUploadClientFatalCount = 0;
$gearmanWorkerSlowCount = 0;


define("PICUPLOADCLIENT_LOG_PATH_TMPL", "/data/site_log/storage/pic-upload/_DATE_/_H_-pic.upload-client.log");
define("PICUPLOADSERVER_LOG_PATH_TMPL", "/data/site_log/storage/pic-upload/_DATE_/_H_-pic.upload-server.log");
define("GEARMANWORKER_ACCESS_LOG_PATH_TMPL", "/data/site_log/storage/gearman/gearman_worker/_DATE_/_H_-gearmanWorkerDaemon-access.log");
define("GEARMANWORKER_ERROR_LOG_PATH_TMPL", "/data/site_log/storage/gearman/gearman_worker/_DATE_/_H_-gearmanWorkerDaemon-error.log");

define("FDFSHTD_LOG_PATH_TMPL", "/data/site_log/storage/gearman/gearman_worker/_DATE_/fastdfs-storage-fdhtd.log");
define("FDFSSTORAGE_LOG_PATH_TMPL", "/data/site_log/storage/gearman/gearman_worker/_DATE_/fastdfs-storage-G-storage.log");
define("FDFSTRACKERD_ERROR_LOG_PATH_TMPL", "/data/site_log/storage/gearman/gearman_worker/_DATE_/fastdfs-storage-G-tracker.log");




class picUploadReadLog{
	static function readPicUploadServerLog( $dateTime, $currentDate, $currentHour, $interval,$hostName="",$timezoneDiff=28800 )
	{
		global $picUploadServerFatalCount;
		$nginxLogTitle = "<font color=green><b>--------------------PIC-UPLOAD-SERVER LOG(begin!)---------------------</b></font>\n\n";
		$msgBody = "";
		$dateTimeInt = $dateTime->getTimestamp();
		$logPath = str_replace("_DATE_", $currentDate, PICUPLOADSERVER_LOG_PATH_TMPL );
		$logPath = str_replace("_H_", $currentHour,$logPath);
		$fileHandler = fopen( $logPath, "r");
		while( $line = fgets($fileHandler) )
		{
			$lineTime = strtotime(substr( $line, strpos( $line, "::" ) -19, 19 ))+$timezoneDiff;
			if ( !Empty( $hostName ) && $hostName == substr( $line, strpos( $line, " " ) ) )
			{
				if ( abs($lineTime-$dateTimeInt) <= $interval )
				{
					if ( strpos( $line, "[fatal]" ) !== false )
					{
						$line = str_replace("[fatal]", "<font color=blue><b>[fatal]</b></b></font>", $line);
						$picUploadServerFatalCount++;
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
					if ( strpos( $line, "[fatal]" ) !== false )
					{
						$line = str_replace("[fatal]", "<font color=blue><b>[fatal]</b></b></font>", $line);
						$picUploadServerFatalCount++;
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
		return $nginxLogTitle.$msgBody."<font color=green><b>--------------------PIC.UPLOAD-SERVER LOG(end!)---------------------</b></font>\n\n";
	}


	static function readPicUploadClientLog( $dateTime, $currentDate, $currentHour, $interval,$hostName="",$timezoneDiff=28800 )
	{
		global $picUploadClientFatalCount;
		$nginxLogTitle = "<font color=green><b>--------------------PIC-UPLOAD-CLIENT LOG(begin!)---------------------</b></font>\n\n";
		$msgBody = "";
		$dateTimeInt = $dateTime->getTimestamp();
		$logPath = str_replace("_DATE_", $currentDate, PICUPLOADCLIENT_LOG_PATH_TMPL );
		$logPath = str_replace("_H_", $currentHour,$logPath);
		$fileHandler = fopen( $logPath, "r");
		while( $line = fgets($fileHandler) )
		{
			$lineTime = strtotime(substr( $line, strpos( $line, "::" ) -19, 19 ))+$timezoneDiff;
			if ( !Empty( $hostName ) && $hostName == substr( $line, strpos( $line, " " ) ) )
			{
				if ( abs($lineTime-$dateTimeInt) <= $interval )
				{
					if ( strpos( $line, "[fatal]" ) !== false )
					{
						$line = str_replace("[fatal]", "<font color=blue><b>[fatal]</b></b></font>", $line);
						$picUploadClientFatalCount++;
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
					if ( strpos( $line, "[fatal]" ) !== false )
					{
						$line = str_replace("[fatal]", "<font color=blue><b>[fatal]</b></b></font>", $line);
						$picUploadClientFatalCount++;
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
		return $nginxLogTitle.$msgBody."<font color=green><b>--------------------PIC.UPLOAD-CLIENT LOG(end!)---------------------</b></font>\n\n";
	}

	static function readGearmanWorkerAccessLog( $dateTime, $currentDate, $currentHour, $interval,$hostName="",$timezoneDiff=28800 )
	{
		global $gearmanWorkerSlowCount;
		$nginxLogTitle = "<font color=green><b>--------------------GEARMAN-WORKER-ACCESS LOG(begin!)---------------------</b></font>\n\n";
		$msgBody = "";
		$dateTimeInt = $dateTime->getTimestamp();
		$logPath = str_replace("_DATE_", $currentDate, GEARMANWORKER_ACCESS_LOG_PATH_TMPL );
		$logPath = str_replace("_H_", $currentHour,$logPath);
		$fileHandler = fopen( $logPath, "r");
		while( $line = fgets($fileHandler) )
		{
			$lineTime = strtotime(substr( $line, strpos( $line, "   " ) + 3, 19 ))+$timezoneDiff;
			if ( !Empty( $hostName ) && $hostName == substr( $line, strpos( $line, " " ) ) )
			{
				if ( abs($lineTime-$dateTimeInt) <= $interval )
				{
					//if ( strpos( $line, "[fatal]" ) !== false )
					if ( floatval($line, strpos( $line, "runTime:" )+8) > 0.5 )
					{
						$line = str_replace("runTime", "<font color=blue><b>[runTime]</b></b></font>", $line);
						$gearmanWorkerSlowCount++;
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
					if ( floatval($line, strpos( $line, "runTime:" )+8) > 0.5 )
					{
						$line = str_replace("runTime", "<font color=blue><b>[runTime]</b></b></font>", $line);
						$gearmanWorkerSlowCount++;
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
		return $nginxLogTitle.$msgBody."<font color=green><b>--------------------GEARMAN-WORKER-ACCESS LOG(end!)---------------------</b></font>\n\n";
	}
	static function readGearmanWorkerErrorLog( $dateTime, $currentDate, $currentHour, $interval,$hostName="",$timezoneDiff=28800 )
	{
		$nginxLogTitle = "<font color=green><b>--------------------GEARMAN-WORKER-ERROR LOG(begin!)---------------------</b></font>\n\n";
		$msgBody = "";
		$dateTimeInt = $dateTime->getTimestamp();
		$logPath = str_replace("_DATE_", $currentDate, GEARMANWORKER_ERROR_LOG_PATH_TMPL );
		$logPath = str_replace("_H_", $currentHour,$logPath);
		$fileHandler = fopen( $logPath, "r");
		while( $line = fgets($fileHandler) )
		{
			$lineTime = strtotime(substr( $line, strpos( $line, "   " ) + 3, 19 ))+$timezoneDiff;
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
		return $nginxLogTitle.$msgBody."<font color=green><b>--------------------GEARMAN-WORKER-ERROR LOG(end!)---------------------</b></font>\n\n";
	}
	static function readFDFSLog( $currentDate )
	{

		$msgBody = "<font color=green><b>--------------------FASTFS-STORAGED LOG(begin!)---------------------</b></font>\n\n";
		$logPath = str_replace("_DATE_", $currentDate, FDFSSTORAGE_LOG_PATH_TMPL );
		$msgBody = $msgBody.file_get_contents($logPath);
		$msgBody = $msgBody."<font color=green><b>--------------------FASTFS-STORAGED LOG(end!)---------------------</b></font>\n\n";
		
		$msgBody .= "<font color=green><b>--------------------FAST-TRACKERD LOG(begin!)---------------------</b></font>\n\n";
		$logPath = str_replace("_DATE_", $currentDate, FDFSTRACKERD_ERROR_LOG_PATH_TMPL );
		$msgBody = $msgBody.file_get_contents($logPath);
		$msgBody = $msgBody."<font color=green><b>--------------------FASTFS-TRACKERD LOG(end!)---------------------</b></font>\n\n";
		
		$msgBody .= "<font color=green><b>--------------------FASTFS-DHTD LOG(begin!)---------------------</b></font>\n\n";
		$logPath = str_replace("_DATE_", $currentDate, FDFSHTD_LOG_PATH_TMPL );
		$msgBody = $msgBody.file_get_contents($logPath);
		$msgBody = $msgBody."<font color=green><b>--------------------FASTFS-DHTD LOG(end!)---------------------</b></font>\n\n";
		
		return $msgBody;
	}

}

?>
