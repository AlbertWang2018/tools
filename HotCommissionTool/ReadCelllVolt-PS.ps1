# Read-HoldingRegisters -Address 127.0.0.1 -Port 502 -Reference 896 -Num 2

# Write-SingleRegister 127.0.0.1 502 908 1
# sleep -second 1
# Write-SingleRegister 127.0.0.1 502 908 0

# 读取 IP 地址文件
$ips = Get-Content -Path "D:\Download\00-CATL\KBESS\HotCommissionTool\IP.txt"
$datetime=Get-Date -Format "yyyyMMdd-HHmmss"
$start=Get-Date
$outputPath = "D:\Download\00-CATL\KBESS\HotCommissionTool\data\CellsVolt-$datetime.csv"
$header="IP,CellsVoltSBMU01,CellsVoltSBMU02,CellsVoltSBMU03,CellsVoltSBMU04,CellsVoltSBMU05"
Out-File -FilePath $outputPath -InputObject $header
# $tw = [System.IO.TextWriter]::Synchronized([System.IO.File]::AppendText($outputPath)) #TextWriter

$ips | ForEach-Object -Parallel {
    $ip = $_    
    $port = 502
    $baseRegister = 1152
    Import-Module "D:\Download\00-CATL\KBESS\HotCommissionTool\PsModbusTcp.ps1"
    
    try {
        # Use a list to collect outputs
        $results = @()
        # Read registers in a batched approach if possible
        $output1 = Read-HoldingRegisters $ip $port $baseRegister 125
        if (-not $output1.Contains("fail")) {
            $results += $output1

            # Use an array of register offsets to read the next register values
            $registerOffsets = @(1277, 1402, 1527, 1024, 2301, 2426, 2551, 3325, 3450, 3575, 4349, 4474, 4599, 5373, 5498, 5623)
            foreach ($offset in $registerOffsets) {
                $registerAddress = $baseRegister + $offset
                $output = Read-HoldingRegisters $ip $port $registerAddress 125
                $results += $output
            }
        }

        # Join results into a single output line
        $output = "$ip, " + ($results -join ", ")
    } catch {
        $output = "$ip connect fail"
    }
} -ThrottleLimit 10 -AsJob | Wait-Job | Receive-Job | Out-File -FilePath $outputPath

# $tw.Close()
$end=Get-Date
$spend=$end-$start
Write-Host "$datetime : 数据已成功写入 $outputPath , 耗时 $spend ;"