from pymodbus.client.sync import ModbusTcpClient
from sys import argv
from concurrent.futures import ThreadPoolExecutor, as_completed

usage = '''
usage:

Depends: pip install pymodbus==2.5.3

Example:
read one register: Modbusrw.exe read 127.0.0.1 502 896 20
read multiple registers: Modbusrw.exe read 127.0.0.1 502 1,401,897
write: Modbusrw.exe write 127.0.0.1 502 896 1

Output will be saved to modbus_results.csv
'''

def process_host(mode, h, port, reg, value=1):
    try:
        client = ModbusTcpClient(h, port)
        client.timeout = 1       
        if mode == 'read':
            if ',' in str(reg):
                res = []
                for r in reg.split(','): 
                    try:
                        value = client.read_holding_registers(address=int(r), count=1).registers[0]
                        res.append(value)
                    except Exception as e:
                        # res.append(str(h)+' failed')
                        res.append('failed')
                        break
                client.close()
                return {'host': h, 'values': res}
            else:
                try:
                    value = client.read_holding_registers(address=int(reg), count=int(value)).registers[0]
                    client.close()
                    return {'host': h, 'values': [str(value)]}
                except Exception as e:
                    return {'host': h, 'values': ['failed']}
        elif mode == 'write': 
            try:
                client.write_register(address=int(reg), value=int(value))
                client.close()
                return {'host': h, 'values': ['OK']}
            except Exception as e:
                return {'host': h, 'values': ['failed']}
        
    except Exception as e:
        return {'host': h, 'status': 'failed', 'error': str(e)}
    finally:
        client.close()

if len(argv) >= 5:
    mode = argv[1]
    host = argv[2]
    port = argv[3]
    reg = argv[4]
    
    if len(argv) > 5:
        value = int(argv[5])
        
    if ',' in str(host):
        hosts = str(host).split(',')
        all_values = []
        
        with ThreadPoolExecutor(max_workers=min(16, len(hosts))) as executor:
            futures = [executor.submit(process_host, mode, h, port, reg, value) for h in hosts]
            for future in as_completed(futures):
                result = future.result()
                all_values.append(result)
        
        # Sort results by host
        sorted_results = sorted(all_values, key=lambda x: x['host'])
        # print(sorted_results)
        # Format output
        output = []
        for result in sorted_results:
            output.append(str(result['values']))
            
        print(';'.join(output).replace('[','').replace(']','').replace("'",'').replace(" ",''))
else:
    print(usage)
