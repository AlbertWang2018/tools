# 读取 IP 地址文件
$ips = Get-Content -Path "D:\Download\00-CATL\KBESS\HotCommissionTool\IP.txt"
$datetime=Get-Date -Format "yyyyMMdd-HHmmss"
$start=Get-Date
$outputPath = "D:\Download\00-CATL\KBESS\HotCommissionTool\CFDisIMM-$datetime.csv"
$tw = [System.IO.TextWriter]::Synchronized([System.IO.File]::AppendText($outputPath))

$ips | ForEach-Object -Parallel {
    $ip = $_
    $pythonPath = "C:\Users\wangw\AppData\Local\Microsoft\WindowsApps\python.exe"  # 根据实际情况修改 Python 路径
    $scriptPath = "D:\Download\00-CATL\KBESS\HotCommissionTool\ModbusRW.py"
    $port = 502
    $mode="write"
    $reg1 = 908 #Fault Clear
    $reg2 = 907 #IMM
    # 调用 Python 脚本并获取输出
    $output = Invoke-Expression "$pythonPath $scriptPath $mode $ip $port $reg1 0"
    $output=$ip+", "+$output
    $writer = $Using:tw
    $writer.WriteLine($output)
	if($output.contains("fail") -eq $False){
        Start-Sleep -second 0.5
        $output = Invoke-Expression "$pythonPath $scriptPath $mode $ip $port $reg1 1"
        $output=$ip+", "+$output
        $writer = $Using:tw
        $writer.WriteLine($output)
        Start-Sleep -second 0.5
        $output = Invoke-Expression "$pythonPath $scriptPath $mode $ip $port $reg2 2"
        $output=$ip+", "+$output
        $writer = $Using:tw
        $writer.WriteLine($output)
        $output = $output.replace("[","").replace("]","").replace("'","")
        # 将结果写入 CSV 文件
        $output=$ip+", "+$output
        $writer = $Using:tw
        $writer.WriteLine($output)
        # echo "已完成$ip, 输出结果为: $out"
	}
}  -ThrottleLimit 6
$tw.Close()
$end=Get-Date
$spend=$end-$start
Write-Host "$datetime : 数据已成功写入 $outputPath , 耗时 $spend ;"