from pymodbus.client.sync import ModbusTcpClient
import sys

USAGE = '''
Usage:

Installation: pip install pymodbus==2.5.3

Example:
To read one register: ModbusRW.py read <IP_ADDRESS> <PORT> <REGISTER> <COUNT>
To read multiple registers: ModbusRW.py read <IP_ADDRESS> <PORT> <REGISTER1>,<REGISTER2>,...<REGISTERN>
To write: ModbusRW.py write <IP_ADDRESS> <PORT> <REGISTER> <VALUE>
'''

def connect_to_modbus_client(host, port):
    """Establish a connection to the Modbus server."""
    client = ModbusTcpClient(host, port)
    if not client.connect():
        print(f"{host}, Connect fail")
        sys.exit(1)
    return client

def read_registers(client, reg, count):
    """Read holding registers from the Modbus server."""
    if ',' in reg:
        results = []
        for register in reg.split(','):
            response = client.read_holding_registers(address=int(register), count=1)
            if response.isError():
                print(f"Error reading register {register}: {response}")
            else:
                results.append(response.registers)
        print(f"{client.host}, {results}")
    else:
        response = client.read_holding_registers(address=int(reg), count=count)
        if response.isError():
            print(f"Error reading register {reg}: {response}")
        else:
            print(f"{client.host}, {response.registers}")

def write_register(client, reg, value):
    """Write a value to a specific register on the Modbus server."""
    response = client.write_register(address=int(reg), value=value)
    if response.isError():
        print(f"Error writing to register {reg}: {response}")
    else:
        print(f"Write success to {reg}")

def main():
    if len(sys.argv) < 5:
        print(USAGE)
        sys.exit(1)

    mode = sys.argv[1].lower()
    host = sys.argv[2]
    port = int(sys.argv[3])  # Ensure port is an integer
    reg = sys.argv[4]
    value = int(sys.argv[5]) if len(sys.argv) > 5 else None

    client = connect_to_modbus_client(host, port)

    try:
        if mode == 'read':
            count = value if value is not None else 1  # Default to reading 1 register if not specified
            read_registers(client, reg, count)
        elif mode == 'write' and value is not None:
            write_register(client, reg, value)
        else:
            print("Invalid command, please specify 'read' or 'write' with the requisite arguments.")
    finally:
        client.close()

if __name__ == '__main__':
    main()