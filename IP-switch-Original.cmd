@echo off
for /f "usebackq delims=" %%i in (`powershell -Command "Get-NetAdapter | Where-Object { $_.Status -eq 'Up' -and ($_.Name -like '*Ethernet*' -or $_.Name -like '*以太网*') } | Select-Object -ExpandProperty Name"`) do (
    set "nic=%%i"
    goto :found
)
:found
netsh interface ip set address name="%nic%" source=static addr=198.120.0.251  mask=255.255.255.0 gateway=198.120.0.1