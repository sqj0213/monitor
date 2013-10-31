<?php

$data1 = file_get_contents($argv[1]);
$arr1 = explode("\n", $data1 );

$outputContentTmpl = "define servicegroup{
	servicegroup_name _SERVICENAME_
        members	_MEMBERS_
}";
$outputContent = "";

$retArr = array();
for ($i=0;$i<count($arr1);$i++)
{
	$tmpVal1 = explode("::",$arr1[$i]);
	if ( !Empty( $tmpVal1[0] ))
	if ( isset($retArr[$tmpVal1[0]]))
		 array_push( $retArr[$tmpVal1[0]],$tmpVal1[1]);
	else
		$retArr[$tmpVal1[0]] = array($tmpVal1[1]);
	
}

while( current($retArr)!=False)
{
	$tmp = current($retArr);
	$serviceName  = key($retArr);
	$members = "";
	for ($j=0;$j<count($tmp);$j++)
	{
		if ( $j == 0 )
			$members = $tmp[$j];
		else
			$members = $members .",".$tmp[$j];
	}
	$outputContent1 = str_replace( '_SERVICENAME_', $serviceName, $outputContentTmpl);
	$outputContent .= "\n".str_replace( '_MEMBERS_', $members, $outputContent1);
	next( $retArr);
}

print_r( $outputContent);
?>
