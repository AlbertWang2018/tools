set /p n=Please input power group No.:
netsh interface ip set address name="Ethernet 2" source=static addr=10.238.%n%.251 mask=255.255.255.0 gateway=10.238.%n%.1 gwmetric=99