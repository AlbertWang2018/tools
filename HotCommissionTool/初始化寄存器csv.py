from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ConnectionException, ModbusIOException

def write_registers(client):
    try:        
        with open('regs.csv','r') as f:
            data=f.read()
        for line in data.splitlines():
            reg, value = line.split(',')
            reg=int(reg)
            value=int(value)
            # 将寄存器地址值写入对应的寄存器
            result = client.write_register(reg, value)
            if isinstance(result, ModbusIOException):
                print(f"写入寄存器 {reg} 失败: {result}")
            # else:
        print(f"成功写入寄存器 {reg}")
    except ConnectionException as e:
        print(f"连接失败: {e}")
    finally:
        client.close()

def main():
    # Modbus TCP 服务器的 IP 地址和端口
    ip_address = '127.0.0.1'
    port = 502

    # 创建 Modbus TCP 客户端
    client = ModbusTcpClient(ip_address, port)

    # 连接到 Modbus TCP 服务器
    if not client.connect():
        print("无法连接到 Modbus TCP 服务器")
        return

    # 写入寄存器
    write_registers(client)

if __name__ == "__main__":
    main()