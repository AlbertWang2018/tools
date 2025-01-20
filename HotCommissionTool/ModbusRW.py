from pymodbus.client.sync import ModbusTcpClient
from sys import argv
import sys

usage = '''
usage:

Depends: pip install pymodbus==2.5.3

Example:
read one register: ModbusWriteData.exe read 127.0.0.1 502 896 20
read multiple registers: ModbusWriteData.exe read 127.0.0.1 502 1,401,897
write: ModbusWriteData.exe write 127.0.0.1 502 896 1
'''

try:
    if len(argv)>=5: 
        mode = argv[1]
        host = argv[2]
        port = argv[3]
        reg = argv[4]
        if len(argv)>5:
            value = int(argv[5])
        client = ModbusTcpClient(host,port)
        client.timeout = 1  # set timeout seconds
        if mode=='read': 
            if ',' in str(reg):
                res=[]
                for reg in reg.split(','): 
                    res.append(client.read_holding_registers(address=int(reg),count=1).registers)
                client.close()
                print(host+', '+str(res).replace('[','').replace(']','').replace(' ',''))
            else:
                print(str(client.read_holding_registers(address=int(reg),count=int(value)).registers).replace('[','').replace(']','').replace(' ',''))
                client.close()
        elif mode=='write': 
            client.write_register(address=int(reg),value=int(value))
            client.close()
            print(host+', '+"Set OK") 
    else:
        print(usage)
except:
    print(host+', Connect fail')
finally:
    client.close()