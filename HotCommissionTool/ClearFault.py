from pymodbus.client.sync import ModbusTcpClient    # 连接失败，用于异常处理
import time,sys
try:
    host = sys.argv[1]
    port = 502
    client = ModbusTcpClient(host,port)

    reg1=908  # 0x38C, Clear Fault
    client.write_register(address=reg1,value=0)
    time.sleep(1)
    client.write_register(address=reg1,value=1)

    # 关闭连接
    client.close()

except:
    print("连接失败")