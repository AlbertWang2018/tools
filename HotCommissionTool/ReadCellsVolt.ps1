# 读取 IP 地址文件
$ips = Get-Content -Path "D:\Download\00-CATL\KBESS\HotCommissionTool\IP.txt"
$datetime=Get-Date -Format "yyyyMMdd-HHmmss"
# Start timing the process
$start = Get-Date
$outputPath = "D:\Download\00-CATL\KBESS\HotCommissionTool\data\CellsVolt-$datetime.csv"
$header = "IP,CellsVoltSBMU01,CellsVoltSBMU02,CellsVoltSBMU03,CellsVoltSBMU04,CellsVoltSBMU05"
Out-File -FilePath $outputPath -InputObject $header

$ips = Get-Content -Path "D:\Download\00-CATL\KBESS\HotCommissionTool\IP.txt"

$ips | ForEach-Object -Parallel {
    $ip = $_
    $pythonPath = "C:\Users\wangw\AppData\Local\Microsoft\WindowsApps\python.exe"
    $scriptPath = "D:\Download\00-CATL\KBESS\HotCommissionTool\ModbusRW.py"
    $port = 502
    $mode = "read"
    
    # Base register address
    $baseRegister = 1152
    $additionalRegisters = @(1277, 1402, 1527, 2301, 2426, 2551, 3325, 3450, 3575, 4349, 4474, 4599, 5373, 5498, 5623)
    $results = @()

    # Read the base register first
    $output1 = & $pythonPath $scriptPath $mode $ip $port $baseRegister 125
    if ($output1 -and -not $output1.Contains("fail")) {
        $results += $output1
        
        # Read additional registers
        foreach ($register in $additionalRegisters) {
            $output = & $pythonPath $scriptPath $mode $ip $port $register 125
            
            if ($output -and -not $output.Contains("fail")) {
                $results += $output
            } else {
                # You might want to handle the 'fail' case here
                $results += "fail"
            }
        }
    } else {
        $results += "fail"
    }

    # Prepare output for CSV
    $output = "$ip, " + ($results -join ", ")
    
    # Append output to the CSV file
    Add-Content -Path $Using:outputPath -Value $output
} -ThrottleLimit 8

$end = Get-Date
$spend = $end - $start
Write-Host "$datetime : Data successfully written to $outputPath. Time spent: $spend."