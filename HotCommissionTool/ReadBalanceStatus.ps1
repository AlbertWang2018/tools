# Read IP address file
$ips = Get-Content -Path "D:\Download\00-CATL\KBESS\HotCommissionTool\IP.txt"
$datetime = Get-Date -Format "yyyyMMdd-HHmmss"
$start = Get-Date
$outputPath = "D:\Download\00-CATL\KBESS\HotCommissionTool\data\BalanceStatus-$datetime.csv"
$header = "IP,BalanceStatusSBMU01,BalanceStatusSBMU02,BalanceStatusSBMU03,BalanceStatusSBMU04,BalanceStatusSBMU05"
Out-File -FilePath $outputPath -InputObject $header

$ips | ForEach-Object -Parallel {
    $ip = $_
    $pythonPath = "C:\Users\wangw\AppData\Local\Microsoft\WindowsApps\python.exe"
    $scriptPath = "D:\Download\00-CATL\KBESS\HotCommissionTool\ModbusRW.py"
    $port = 502
    $mode = "read"
    $baseRegister = 1936
    $numRegisters = 5
    $registersResults = @()

    # Collect outputs
    for ($i = 0; $i -lt $numRegisters; $i++) {
        $registerAddress = $baseRegister + ($i * 1024)
        $output = & $pythonPath $scriptPath $mode $ip $port $registerAddress 48
        
        # Check for "fail" directly
        if (-not $output1.Contains("fail")) {
            break
        }
        # Clean the output and add it to the results
        $output = $output -replace "[$$']", ""  # Remove brackets and single quotes
        $registersResults += $output
    }

    # Build the output line
    $output = "$ip, " + ($registersResults -join ", ")
    
    # Write output to CSV
    Add-Content -Path $Using:outputPath -Value $output
} -ThrottleLimit 8

$end = Get-Date
$spend = $end - $start
Write-Host "$datetime : Data successfully written to $outputPath. Time spent: $spend."
