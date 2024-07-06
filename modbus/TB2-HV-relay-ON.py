from pymodbus.client.sync import ModbusTcpClient    # 连接失败，用于异常处理
import time,sys

try:
    host = sys.argv[1]
    port = 502
    client = ModbusTcpClient(host,port)

    reg1=897  # 0x381, HV relay
    client.write_register(address=reg1,value=2)

    # 关闭连接
    client.close()

except:
    print("连接失败")