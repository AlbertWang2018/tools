from pymodbus.client import ModbusTcpClient
from sys import argv
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logging.disable(logging.CRITICAL)

usage = '''
usage:

Depends: pip install pymodbus

Example:
read one register: python modbusRW1.py read 127.0.0.1 502 896 20
read multiple registers: python modbusRW1.py read 127.0.0.1,192.168.1.1 502 17,36,897
write: python modbusRW1.py write 127.0.0.1 502 896 1

Output will be saved to modbus_results.csv
'''

def process_host(mode, h, port, reg, value=1):
    try:
        client = ModbusTcpClient(h, port=int(port))
        client.timeout = 0.5
        if mode == 'read':
            if ',' in str(reg):
                res = []
                for r in reg.split(','): 
                    try:
                        rv = client.read_holding_registers(address=int(r), count=int(value)).registers[0]
                        res.append(str(rv))
                    except Exception as e:
                        res.append('failed')
                        break
                client.close()
                return {'host': h, 'values': res}
            else:
                try:
                    rv = str(client.read_holding_registers(address=int(reg),count=int(value)).registers).replace('[','').replace(']','').replace(' ','')
                    client.close()
                    return {'host': h, 'values': str(rv)}
                except Exception as e:
                    return {'host': h, 'values': 'failed'}
        elif mode == 'write': 
            try:
                client.write_register(address=int(reg), value=int(value))
                client.close()
                return {'host': h, 'values': 'OK'}
            except Exception as e:
                return {'host': h, 'values': 'failed'}
    except Exception as e:
        return {'host': h, 'values': 'failed'}

def main():
    if len(argv) >= 5:
        mode = argv[1]
        host = argv[2]
        port = argv[3]
        reg = argv[4]    
    if len(argv) == 6:
        value = int(argv[5])
            
        if ',' in str(host):
            hosts = str(host).split(',')
            all_values = []        
            with ThreadPoolExecutor(max_workers=min(16, len(hosts))) as executor:
                if(mode=='read'):
                    futures = [executor.submit(process_host, mode, h, port, reg, value) for h in hosts]
                if(mode=='write'):
                    futures = [executor.submit(process_host, mode, h, port, reg, value) for h in hosts]
                for future in as_completed(futures):
                    result = future.result()
                    all_values.append(result)        
            # Sort results by host and formating output
            sorted_results = sorted(all_values, key=lambda x: x['host'])
            output = []
            if(len(sorted_results)) > 0:
                for result in sorted_results:
                    output.append(str(result['values']))            
            print(';'.join(output).replace('[','').replace(']','').replace("'",'').replace(" ",''))
            return {}
        elif(mode=='read' and (not ',' in str(host))):
            res = process_host(mode, host, port, reg, value)
            print(str(res['values']).replace('[','').replace(']','').replace("'",'').replace(" ",''))
            return {}
        elif(mode=='write' and (not ',' in str(host))):
            res = process_host(mode, host, port, reg, value)
            print(str(res['values']).replace('[','').replace(']','').replace("'",'').replace(" ",''))
            return {}
    else:
        print(usage)

if __name__=="__main__":
    main()