https://www.123pan.com/s/A6cA-BnoJh

Download MSVC Runtime all in one from above.

1. VC runtime;
2. ZLG USB CAN drive;
3. ESS config, select device is USBCAN;

默认打开就是管理员权限：
用dnspy打开ESSServer.exe, ESSServer模块下面查找PClassAll，里面 "普通用户" 上面几行，LoginUserLevel默认是3，改为1就OK。
