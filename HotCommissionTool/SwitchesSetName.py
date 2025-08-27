import csv
import asyncio
import telnetlib3

CSV_FILE = 'switchesIP_Name.csv'
TELNET_PORT = 23
USERNAME = 'admin'
PASSWORD = 'admin'
COMMAND_1 = 'Information'
COMMAND_2 = 'Config -n {}'
COMMAND_3 = 'show mac'
COMMAND_4 = 'manage'
COMMAND_5 = 'IP {} 255.255.255.0'

async def telnet_switch(ip, name):
    try:
        reader, writer = await telnetlib3.open_connection(ip, TELNET_PORT, connect_minwait=1)
        await asyncio.sleep(1)
        await reader.readuntil(b'Username:')
        writer.write(USERNAME + '\n')
        await asyncio.sleep(0.5)
        await reader.readuntil(b'Password:')
        writer.write(PASSWORD + '\n')
        await asyncio.sleep(0.5)
        writer.write(COMMAND_1 + '\n')
        await asyncio.sleep(0.5)
        writer.write(COMMAND_2.format(name) + '\n')
        await asyncio.sleep(0.5)
        writer.write('exit\n')
        writer.close()
        print(f"{ip} ({name}) 配置完成")
    except Exception as e:
        print(f"{ip} ({name}) 配置失败: {e}")

async def main():
    tasks = []
    with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) < 2:
                continue
            ip, name = row[0].strip(), row[1].strip()
            tasks.append(telnet_switch(ip, name))
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())