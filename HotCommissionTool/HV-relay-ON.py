from pymodbus.client.sync import ModbusTcpClient    # 连接失败，用于异常处理
from time import sleep; from sys import argv

try:
    host = argv[1]
    port = 502
    client = ModbusTcpClient(host,port)

    reg=897  # 0x381, HV relay
    client.write_register(address=reg,value=2)
    sleep(2)
    status=client.read_holding_registers(address=reg,count=1)
    if status.registers[0]==2:
        client.write_register(address=reg,value=1)
        print("HV relay turn ON and Hold sucessful")

    # 关闭连接
    client.close()

except:
    print("connect fail")