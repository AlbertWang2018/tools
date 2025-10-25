如果管理员cmd窗口运行 winget install vcredist 不行，可以从这里下载安装vc运行库：
Download MSVC Runtime all in one from here：https://www.123pan.com/s/A6cA-BnoJh

Install .Net3.5:  Dism /online /Enable-Feature /FeatureName:"NetFx3"

OpenModScan: https://github.com/sanny32/OpenModScan  ( msiexec.exe -i https://github.com/sanny32/OpenModScan/releases/download/1.11.1/qt5-omodscan_1.11.1-1_amd64.exe )

1. VC runtime;
2. ZLG USB CAN drive; (The memory integrity check feature needs to be turned off. )
3. ESS config, select device is USBCAN;

ESS Admin default：
dnspy->ESSServer.exe->ESSServer->PClassAll->"普通用户"->LoginUserLevel->3 to 1.


javascript:(function(){try{var input=prompt("Input PI num：");var num=parseInt(input);if(isNaN(num)){alert("Please enter a valid number！");return;}var x=Math.floor((num-1)/9)+1;var y=((num-1)%9)+1+"1";var newIP="10.238."+x+"."+y;var originalURL="http://10.238.2.11/tc3plchmiweb/port_851/visu/webvisu.htm";var newURL=originalURL.replace("10.238.2.11",newIP);var newWindow=window.open();newWindow.location.href=newURL;}catch(e){alert("error："+e.message);}})();


javascript:(function(){var pi = prompt("Enter PI number (1-160):");  pi = parseInt(pi);  if (pi < 1 || pi > 160 || isNaN(pi)) {    alert("Invalid PI number. Must be between 1 and 160.");    return;  }  var pg = Math.floor((pi - 1) / 8) + 1;  var second = pg <= 10 ? 149 : 249;  var third = 101 + ((pg - 1) % 10);  var last = 110 + ((pi - 1) % 8) * 10;  var url = "http://10." + second + "." + third + "." + last + "/tc3plchmiweb/port_851/visu/webvisu.htm";  window.open(url, "_blank");})();
