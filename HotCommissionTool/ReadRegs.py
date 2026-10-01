import asyncio
import os
from datetime import datetime
import logging
from concurrent.futures import ThreadPoolExecutor
from pymodbus.client import ModbusTcpClient

logging.disable(logging.CRITICAL)

regfile="RegSbmu.csv"

header_parts = ["IP"]
registers_parts = []
try:
    with open(regfile, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(",")
                if len(parts) >= 3:
                    registers_parts.append(parts[1].strip())
                    header_parts.append(parts[2].strip())
    header = ",".join(header_parts)
    registers_str = ",".join(registers_parts)
except Exception as e:
    print(f"Error reading {regfile}: {e}")
    header = "IP"
    registers_str = ""

# Parse registers once
REGISTERS = [int(r) for r in registers_str.split(',')] if registers_str else []

# Group contiguous registers into blocks (start_address, count) for efficient reading
REGISTER_BLOCKS = []
if REGISTERS:
    start_addr = REGISTERS[0]
    count = 1
    for i in range(1, len(REGISTERS)):
        # If continuous AND within common Modbus limits (e.g., 125 registers)
        if REGISTERS[i] == REGISTERS[i-1] + 1 and count < 125:
            count += 1
        else:
            REGISTER_BLOCKS.append((start_addr, count))
            start_addr = REGISTERS[i]
            count = 1
    REGISTER_BLOCKS.append((start_addr, count))

def read_modbus_sync(ip, port=502):
    """
    Synchronous function to read modbus registers in blocks.
    To be run in a thread pool.
    """
    try:
        client = ModbusTcpClient(ip, port=port)
        client.timeout = 2  # set timeout seconds
        if not client.connect():
            return [ip] + ["fail"] * len(REGISTERS)
        
        res = []
        for start_addr, count in REGISTER_BLOCKS:
            # Grouped reading: efficient when addresses are contiguous
            rr = client.read_holding_registers(address=start_addr, count=count)
            if rr.isError():
                res.extend(["Err"] * count)
            else:
                res.extend([str(val) for val in rr.registers])
        
        client.close()
        return [ip] + res
    except Exception as e:
        return [ip] + ["fail"] * len(REGISTERS)

async def main():
    dt = datetime.now().strftime("%Y%m%d-%H%M%S")
    if not os.path.exists("data"):
        os.makedirs("data")
    file_path = f".\\data\\Data_{dt}.csv"

    # Read IPs
    try:
        with open("IP.txt", "r") as f:
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
    # Process results into a consistent list of lists
    data = []
    for row in results:
        if isinstance(row, list):
            data.append([str(item) for item in row])
        else:
            # Handle any legacy string results (though read_modbus_sync now always returns list)
            data.append(str(row).split(","))

    header_list = header.split(",")
    # Combine header and data
    all_rows = [header_list] + data
    # Sort data rows (excluding header) by IP (first column)
    sorted_rows = [all_rows[0]] + sorted(all_rows[1:], key=lambda x: x[0] if len(x) > 0 else "")
    # Write to CSV
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        for row in sorted_rows:
            f.write(",".join(row) + "\r\n")

    print(f"{dt}: data has been written to {file_path}, Total time: {datetime.now() - Start}")

if __name__ == "__main__":
    Start = datetime.now()
    asyncio.run(main())