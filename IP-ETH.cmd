@echo off
set /p n=Please input power group No.:
for /f "usebackq delims=" %%i in (`powershell -Command "Get-NetAdapter | Where-Object { $_.Status -eq 'Up' -and ($_.Name -like '*Ethernet*' -or $_.Name -like '*以太网*') } | Select-Object -ExpandProperty Name"`) do (
    set "nic=%%i"
    goto :found
)
:found
netsh interface ip set address name="%nic%" source=static addr=10.149.10%n%.250 mask=255.255.255.0 gateway=10.149.10%n%.1 gwmetric=99