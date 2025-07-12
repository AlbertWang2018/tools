import sys
from time import sleep
import subprocess as sp

def set_ip(interface, ip_address):
    # Windows命令：netsh interface ip set address
    cmd = [
        "netsh", "interface", "ip", "set", "address",
        f"name={interface}", "static", ip_address, "255.255.255.0",ip_address.split('.')[0] + '.' + ip_address.split('.')[1] + '.' + ip_address.split('.')[2] + '.1'
    ]
    try:
        sp.run(cmd, check=True)        
        print(f"IP地址已设置为 {ip_address} 在网卡 {interface}")
    except sp.CalledProcessError as e:
        print("设置IP地址失败:", e)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python SetIp.py <网卡名称> <IP地址>")
        sys.exit(1)
    interface = sys.argv[1]
    ip_address = sys.argv[2]
    set_ip(interface, ip_address)