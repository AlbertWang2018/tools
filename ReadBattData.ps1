$batt=(Get-WmiObject -Namespace 'root\wmi' -Class batterystatus)
$c=$batt.chargerate[0]/1000
$v=$batt.voltage[0]/1000
$r=$batt.remainingcapacity[0]/1000
echo "$c W, $v V, $r Wh"
sleep -Seconds 3