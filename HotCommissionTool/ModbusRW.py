from pymodbus.client.sync import ModbusTcpClient
from sys import argv

usage = '''
usage:

Depends: pip install pymodbus==2.5.3

Example:
read: ModbusWriteData.exe read 127.0.0.1 502 896 20
write: ModbusWriteData.exe write 127.0.0.1 502 896 1
'''

try:    
    if len(argv)<5: 
        print(usage)
    else:
        mode = argv[1]
        host = argv[2]
        port = argv[3]
        reg = int(argv[4])  # 896,Beat Heart
        value = int(argv[5])
        client = ModbusTcpClient(host,port)
        if argv[1]=='read': 
            print(client.read_holding_registers(address=reg,count=value).registers)
        if argv[1]=='write': 
            client.write_register(address=reg,value=value)
            print("Write success")
except:
    print("Connect fail")