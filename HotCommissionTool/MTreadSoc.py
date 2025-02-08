import threading
import queue
import subprocess
import pandas as pd
from datetime import datetime

header = "IP,soc,volt,I,MaxVc,MinVc,AvgVc,soc1,soc2,soc3,soc4,soc5,volt1,volt2,volt3,volt4,volt5," \
         "warn1,warn2,SysSta,IMM,SOCMaintReq,RemainCharge1,RemainDischarge1,HisChargeCapL1," \
         "HisChargeCapH1,HisDischargeCapL1,HisDischargeCapH1,RemainCharge2,RemainDischarge2," \
         "HisChargeCapL2,HisChargeCapH2,HisDischargeCapL2,HisDischargeCapH2,RemainCharge3," \
         "RemainDischarge3,HisChargeCapL3,HisChargeCapH3,HisDischargeCapL3,HisDischargeCapH3," \
         "RemainCharge4,RemainDischarge4,HisChargeCapL4,HisChargeCapH4,HisDischargeCapL4," \
         "HisDischargeCapH4,RemainCharge5,RemainDischarge5,HisChargeCapL5,HisChargeCapH5," \
         "HisDischargeCapL5,HisDischargeCapH5,EnvTemp,auxpl,ChrgSOE,DisChrgSOE,CSOC1,DSOC1,CSOC2,DSOC2,CSOC3,DSOC3,CSOC4,DSOC4,CSOC5,DSOC5,TMSOutWT,TMSInWT,TMSRealMode"

registers = "34,32,33,36,37,38,1059,2083,3107,4131,5155,1057,2081,3105,4129,5153," \
            "16,17,770,907,68,1078,1079,1108,1109,1110,1111,2102,2103,2132,2133," \
            "2134,2135,3126,3127,3156,3157,3158,3159,4150,4151,4180,4181,4182," \
            "4183,5174,5175,5204,5205,5206,5207,56,898,47,48,1076,1077,2100,2101,3124,3125,4148,4149,5172,5173,108,109,107"

# Function to execute the modbus command
def modbus_rw_task(q, command):
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        q.put(result)
    except Exception as e:
        q.put(f"Error: {e}")

def main():
    dt = datetime.now().strftime("%Y%m%d-%H%M%S")
    file_path = f"D:\\Download\\00-CATL\\KBESS\\HotCommissionTool\\data\\SocVolt-{dt}.csv"

    # Collect commands based on IPs
    commands = []
    with open("D:\\Download\\00-CATL\\KBESS\\HotCommissionTool\\IP.txt", "r") as f:
        ip_lines = f.readlines()

    # Generate command for each IP
    for ip in ip_lines:
        command = f"python ModbusRW.py read {ip.strip()} 502 {registers}"
        commands.append(command)

    # Create a queue and thread pool
    q = queue.Queue()
    from concurrent.futures import ThreadPoolExecutor
    
    # Create and run threads with max 6 concurrent
    with ThreadPoolExecutor(max_workers=min(18, len(ip_lines))) as executor:
        futures = [executor.submit(modbus_rw_task, q, cmd) for cmd in commands]
        
        # Wait for all futures to complete
        for future in futures:
            future.result()

    # Collect results without redundant processing
    results = []
    while not q.empty():
        result = q.get().replace('[', '').replace(']', '').replace("'", "").replace('"', '').replace("\n", "")
        results.append(result)

    # Write results to CSV and sort directly
    data = [row.split(",") for row in results]  # Convert each result to a list
    header_list = header.split(",")  # Split header for DataFrame creation
    df = pd.DataFrame(data, columns=header_list)  # Create DataFrame from results
    sorted_df = df.sort_values(by='IP')  # Sort by the first column (IP)

    # Write sorted data to a new CSV file
    sorted_df.to_csv(file_path, index=False)

    print(f"{dt}: data has been written to {file_path}, Total time: {datetime.now()-Start}")

if __name__ == "__main__":
    Start = datetime.now()
    main()
