import asyncio
import os
from datetime import datetime
import logging
from concurrent.futures import ThreadPoolExecutor
from pymodbus.client import ModbusTcpClient

logging.disable(logging.CRITICAL)

header = "IP,soc,volt,I,MaxVc,MinVc,AvgVc,soc1,soc2,soc3,soc4,soc5,volt1,volt2,volt3,volt4,volt5," \
         "warn16,warn17,SysSta,IMM,SOCMaintReq,RemainCharge1,RemainDischarge1,HisChargeCapL1," \
         "HisChargeCapH1,HisDischargeCapL1,HisDischargeCapH1,RemainCharge2,RemainDischarge2," \
         "HisChargeCapL2,HisChargeCapH2,HisDischargeCapL2,HisDischargeCapH2,RemainCharge3," \
         "RemainDischarge3,HisChargeCapL3,HisChargeCapH3,HisDischargeCapL3,HisDischargeCapH3," \
         "RemainCharge4,RemainDischarge4,HisChargeCapL4,HisChargeCapH4,HisDischargeCapL4," \
         "HisDischargeCapH4,RemainCharge5,RemainDischarge5,HisChargeCapL5,HisChargeCapH5," \
         "HisDischargeCapL5,HisDischargeCapH5,EnvTemp,auxpl,ChrgSOE,DisChrgSOE,CSOC1,DSOC1," \
         "CSOC2,DSOC2,CSOC3,DSOC3,CSOC4,DSOC4,CSOC5,DSOC5,TMSOutWT,TMSInWT,TMSRealMode,Dehum2," \
         "SBMUWarn5,SBMUWarn6,TmsFaultCode,MaxCellTemp,MaxCTPosition,SSV1,SSV2,SSV3,SSV4,SSV5," \
         "CS1,CS2,CS3,CS4,CS5,StrEn,SC0,SC2,MinVc1,MinVc2,MinVc3,MinVc4,MinVc5"

registers_str = "34,32,33,36,37,38,1059,2083,3107,4131,5155,1057,2081,3105,4129,5153," \
                "16,17,770,907,68,1078,1079,1108,1109,1110,1111,2102,2103,2132,2133," \
                "2134,2135,3126,3127,3156,3157,3158,3159,4150,4151,4180,4181,4182," \
                "4183,5174,5175,5204,5205,5206,5207,56,898,47,48,1076,1077," \
                "2100,2101,3124,3125,4148,4149,5172,5173,108,109,107,18,5,6,111," \
                "1064,1074,1080,2104,3128,4152,5176,1135,2159,3183,4207,5231,909,0,2,1062,2086,3110,4134,5158"

# Parse registers once
REGISTERS = [int(r) for r in registers_str.split(',')]

def read_modbus_sync(ip, port=502):
    """
    Synchronous function to read modbus registers.
    To be run in a thread pool.
    """
    try:
        client = ModbusTcpClient(ip, port=port)
        client.timeout = 1  # set timeout seconds
        if not client.connect():
            return f"{ip}, fail"
        
        res = []
        for reg in REGISTERS:
            # Reading 1 register at a time as per original logic
            # Optimization: Could potentially read contiguous blocks if supported by device
            rr = client.read_holding_registers(address=reg, count=1)
            if rr.isError():
                res.append("Err")
            else:
                res.append(str(rr.registers[0]))
        
        client.close()
        return [ip] + res
    except Exception as e:
        return f"{ip}, fail"

async def main():
    dt = datetime.now().strftime("%Y%m%d-%H%M%S")
    if not os.path.exists("data"):
        os.makedirs("data")
    file_path = f".\\data\\SocVolt_F2_{dt}.csv"

    # Read IPs
    try:
        with open("IP-F2.txt", "r") as f:
            ip_lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print("Error: IP.txt not found.")
        return

    loop = asyncio.get_running_loop()
    # Use a ThreadPoolExecutor to run the synchronous modbus calls
    # Adjust max_workers based on network capacity, 50-100 is usually fine for IO bound
    max_workers = min(128, len(ip_lines)) if len(ip_lines) > 0 else 1
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        tasks = [
            loop.run_in_executor(executor, read_modbus_sync, ip)
            for ip in ip_lines
        ]
        results = await asyncio.gather(*tasks)

    # Write results to CSV and sort directly
    data = [str(row).replace('[', '').replace(']', '').replace("'", "").replace('"', '').split(",") for row in results]  # Convert each result to a list
    header_list = header.split(",")  # Split header for DataFrame creation

    # Write results to CSV and sort directly without pandas
    # Combine header and data
    all_rows = [header_list] + data
    # Sort data rows (excluding header) by IP (first column)
    sorted_rows = [all_rows[0]] + sorted(all_rows[1:], key=lambda x: x[0])
    # Write to CSV
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        for row in sorted_rows:
            f.write(",".join(row) + "\n")

    print(f"{dt}: data has been written to {file_path}, Total time: {datetime.now() - Start}")

if __name__ == "__main__":
    Start = datetime.now()
    asyncio.run(main())