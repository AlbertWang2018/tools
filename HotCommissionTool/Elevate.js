var command = WScript.Arguments.Item(0);
var argument = "";
argument = '"'+WScript.Arguments.Item(1)+'"'
try{
	var shellapp = new ActiveXObject("Shell.Application");
	shellapp.ShellExecute(command, argument, null, "runas", 1);
}
catch(e){
	~ WScript.Echo("Something wrong: " + e.description);
}