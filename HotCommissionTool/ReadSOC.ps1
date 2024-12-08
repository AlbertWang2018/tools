# Read IP address file
$ips = Get-Content -Path "D:\Download\00-CATL\KBESS\HotCommissionTool\IP.txt"
$datetime = Get-Date -Format "yyyyMMdd-HHmmss"
$start = Get-Date
$outputPath = "D:\Download\00-CATL\KBESS\HotCommissionTool\data\SocVolt-$datetime.csv"
$header = "IP,soc,volt,I,MaxVc,MinVc,AvgVc,soc1,soc2,soc3,soc4,soc5,volt1,volt2,volt3,volt4,volt5,warn1,warn2,SysSta,IMM,SOCMaintReq,RemainCharge1,RemainDischarge1,HisChargeCapL1,HisChargeCapH1,HisDischargeCapL1,HisDischargeCapH1,RemainCharge2,RemainDischarge2,HisChargeCapL2,HisChargeCapH2,HisDischargeCapL2,HisDischargeCapH2,RemainCharge3,RemainDischarge3,HisChargeCapL3,HisChargeCapH3,HisDischargeCapL3,HisDischargeCapH3,RemainCharge4,RemainDischarge4,HisChargeCapL4,HisChargeCapH4,HisDischargeCapL4,HisDischargeCapH4,RemainCharge5,RemainDischarge5,HisChargeCapL5,HisChargeCapH5,HisDischargeCapL5,HisDischargeCapH5,EnvTemp"
Out-File -FilePath $outputPath -InputObject $header

$ips | ForEach-Object -Parallel {
    $ip = $_
    $pythonPath = "C:\Users\wangw\AppData\Local\Microsoft\WindowsApps\python.exe"  # Adjust Python path as necessary
    $scriptPath = "D:\Download\00-CATL\KBESS\HotCommissionTool\ModbusRW.py"
    $registers = "34,32,33,36,37,38,1059,2083,3107,4131,5155,1057,2081,3105,4129,5153,16,17,770,907,68,1078,1079,1108,1109,1110,1111,2102,2103,2132,2133,2134,2135,3126,3127,3156,3157,3158,3159,4150,4151,4180,4181,4182,4183,5174,5175,5204,5205,5206,5207,56"

    # Invoke the Python script and capture output
    $output = & $pythonPath $scriptPath read $ip 502 $registers
    if (-not $output1.Contains("fail")) {
        # Clean output
        $output = $output -replace "[$$']", ""
        
        # Combine IP with result
        $output = "$ip, $output"
        
        # Write output to CSV
        Add-Content -Path $Using:outputPath -Value $output
    }
} -ThrottleLimit 8

$end = Get-Date
$spend = $end - $start
Write-Host "$datetime : Data written to $outputPath successfully, Time spent: $spend;"