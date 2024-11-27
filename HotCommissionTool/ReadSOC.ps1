# 读取 IP 地址文件
$ips = Get-Content -Path "D:\Download\00-CATL\KBESS\HotCommissionTool\IP.txt"
$datetime=Get-Date -Format "yyyyMMdd-HHmmss"
$start=Get-Date
$outputPath = "D:\Download\00-CATL\KBESS\HotCommissionTool\SocVolt-$datetime.csv"
$tw = [System.IO.TextWriter]::Synchronized([System.IO.File]::AppendText($outputPath)) #TextWriter
$writer = $Using:tw
$header="IP,soc,volt,soc1,soc2,soc3,soc4,soc5,volt1,volt2,volt3,volt4,volt5,warn1,warn2,SysSta,IMM"
$writer = $Using:tw
$writer.WriteLine($header)

$ips | ForEach-Object -Parallel {
    $ip = $_
    $pythonPath = "C:\Users\wangw\AppData\Local\Microsoft\WindowsApps\python.exe"  # 根据实际情况修改 Python 路径
    $scriptPath = "D:\Download\00-CATL\KBESS\HotCommissionTool\ModbusRW.py"
    $port = 502
    $mode="read"
    $registers = "34,32,1059,2083,3107,4131,5155,1057,2081,3105,4129,5153,16,17,770,907"
    # 调用 Python 脚本并获取输出
    $output = Invoke-Expression "$pythonPath $scriptPath $mode $ip $port $registers"
    $output = $output.replace("[","").replace("]","").replace("'","")
    # 将结果写入 CSV 文件
    $output=$ip+", "+$output
    $writer = $Using:tw
    $writer.WriteLine($output)
    # echo "已完成$ip, 输出结果为: $out"
}  -ThrottleLimit 6
$tw.Close()
$end=Get-Date
$spend=$end-$start
Write-Host "$datetime : 数据已成功写入 $outputPath , 耗时 $spend ;"