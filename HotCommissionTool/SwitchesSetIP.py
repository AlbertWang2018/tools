import csv,time
import asyncio
import telnetlib3

CSV_FILE = 'switchesIP_MAC.csv'
Host = '10.249.37.196'
TELNET_PORT = 23
USERNAME = 'admin'
PASSWORD = 'admin'
COMMAND_1 = 'Information'
COMMAND_2 = 'Config -n {}'
COMMAND_3 = 'show mac'
COMMAND_4 = 'manage'
COMMAND_5 = 'IP {} 255.255.255.0'

async def telnet_switch():
    try:
        reader, writer = await telnetlib3.open_connection(Host, TELNET_PORT, connect_minwait=1)
        await asyncio.sleep(1)
        await reader.readuntil(b'Username:')
        writer.write(USERNAME + '\n')
        await asyncio.sleep(0.5)
        await reader.readuntil(b'Password:')
        writer.write(PASSWORD + '\n')
        await asyncio.sleep(0.5)
        writer.write(COMMAND_1 + '\n')
        await asyncio.sleep(0.5)
        writer.write(COMMAND_3 + '\n')
        await asyncio.sleep(0.5)
        mac1=await reader.read(500)
        mac=mac1.split(':')[1][13:18].replace('.','')
        # print(mac)
        # 根据mac查找对应的ip
        ip_from_csv = None
        with open(CSV_FILE, encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                if len(row) < 2:
                    continue
                if row[0].strip().lower() == mac.strip().lower():
                    ip_from_csv = row[1].strip()
                    name = row[2].strip()
                    break
        if ip_from_csv:
            print(f"查表得到 {mac} 的IP为 {ip_from_csv}")             
            writer.write('exit\n')
            await asyncio.sleep(0.5)
            writer.write(COMMAND_4 + '\n')
            await asyncio.sleep(0.5)
            writer.write(COMMAND_5.format(ip_from_csv) + '\n')
        else:
            print(f"未在CSV中找到 {mac} 的IP")
        # writer.write(COMMAND_2.format(name) + '\n')
        await asyncio.sleep(0.5)
        writer.write('exit\n')
        await asyncio.sleep(0.5)
        writer.write('quit\n')
        writer.close()
        reader.close()
        print(f"{mac} ({ip_from_csv}) {name} 配置完成")
    except Exception as e:
        print(f"配置失败: {e}")

if __name__ == '__main__':
    i=0
    while i<2:
        print(i)
        asyncio.run(telnet_switch())
        i+=1