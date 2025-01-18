如果管理员cmd窗口运行 winget install vcredist 不行，可以从这里下载安装vc运行库：
Download MSVC Runtime all in one from here：https://www.123pan.com/s/A6cA-BnoJh

OpenModScan: https://github.com/sanny32/OpenModScan

1. VC runtime;
2. ZLG USB CAN drive;
3. ESS config, select device is USBCAN;

ESS Admin default：
dnspy->ESSServer.exe->ESSServer->PClassAll->"普通用户"->LoginUserLevel->3 to 1.


javascript:(function(){try{var input=prompt("Input PI num：");var num=parseInt(input);if(isNaN(num)){alert("Please enter a valid number！");return;}var x=Math.floor((num-1)/9)+1;var y=((num-1)%9)+1+"1";var newIP="10.238."+x+"."+y;var originalURL="http://10.238.2.11/tc3plchmiweb/port_851/visu/webvisu.htm";var newURL=originalURL.replace("10.238.2.11",newIP);var newWindow=window.open();newWindow.location.href=newURL;}catch(e){alert("error："+e.message);}})();
