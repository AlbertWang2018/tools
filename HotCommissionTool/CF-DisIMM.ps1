# Read IP address file
$ips = Get-Content -Path "D:\Download\00-CATL\KBESS\HotCommissionTool\IP.txt"
$datetime = Get-Date -Format "yyyyMMdd-HHmmss"
$start = Get-Date
$outputPath = "D:\Download\00-CATL\KBESS\HotCommissionTool\data\CFDisIMM-$datetime.csv"

# Create a synchronized writer for CSV output
$tw = [System.IO.TextWriter]::Synchronized([System.IO.File]::AppendText($outputPath))

$pythonPath = "C:\Users\wangw\AppData\Local\Microsoft\WindowsApps\python.exe"  # Adjust Python path as necessary
$scriptPath = "D:\Download\00-CATL\KBESS\HotCommissionTool\ModbusRW.py"
$port = 502
$mode = "write"
$reg1 = 908  # Fault Clear
$reg2 = 907  # IMM

$ips | ForEach-Object -Parallel {
    $ip = $_
    
    # Call Python script and get output
    $output = Invoke-Expression "$Using:pythonPath $Using:scriptPath $Using:mode $ip $Using:port $Using:reg1 0"
    
    if (-not $output.contains("fail")) {
        Start-Sleep -Seconds 0.1
        $output += ", " + (Invoke-Expression "$Using:pythonPath $Using:scriptPath $Using:mode $ip $Using:port $Using:reg1 1")
        $output += ", " + (Invoke-Expression "$Using:pythonPath $Using:scriptPath $Using:mode $ip $Using:port $Using:reg2 2")
        $output = $output -replace "[$$']", ""  # Replace unwanted characters
    } else {
        $output = "fail"
    }
    
    # Write result to CSV file
    $output = "$ip, $output"
    $writer = $Using:tw
    $writer.WriteLine($output)
} -ThrottleLimit 8

$tw.Close()
$end = Get-Date
$spend = $end - $start
Write-Host "$datetime : Data has been successfully written to $outputPath, elapsed time: $spend ;"
