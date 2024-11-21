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
        if len(argv)>5:
            value = int(argv[5])
        client = ModbusTcpClient(host,port)
        if mode=='write': 
            reg = int(argv[4])  # 896,Beat Heart
            client.write_register(address=reg,value=value)
            print("Write success")        
        if mode=='read': 
            if ',' in str(argv[4]):
                res=[]
                for reg in argv[4].split(','): 
                    res.append(str(client.read_holding_registers(address=int(reg),count=1).registers).replace('[','').replace(']','').replace(' ',''))
                print(res)
            else:
                reg = int(argv[4])
                print(str(client.read_holding_registers(address=int(reg),count=value).registers).replace('[','').replace(']','').replace(' ',''))
        client.close()
except:
    print("Connect fail")