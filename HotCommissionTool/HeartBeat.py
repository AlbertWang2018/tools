from pymodbus.client.sync import ModbusTcpClient
import time,sys

try:
    host = sys.argv[1]
    port = 502
    client = ModbusTcpClient(host,port)

    reg1=896  # Beat Heart
    i=0;j=255
    while True:
        client.write_register(address=reg1,value=i)
        if i<j:
            i+=1
        else:
            i=0
        time.sleep(1)
except:
    print("连接失败")