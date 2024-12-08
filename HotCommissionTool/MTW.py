import threading
import queue
import time
import subprocess
from datetime import datetime

file = f"D:\\Download\\00-CATL\\KBESS\\HotCommissionTool\\data\\CF-DisIMM-{datetime.now().strftime('%Y%m%d-%H%M%S')}.csv"

def modbus_rw_task(q, command):
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        q.put(result)
    except Exception as e:
        q.put(f"Error: {e}")

def main():
    # Define commands to execute
    commands = []
    with open(r"D:\Download\00-CATL\KBESS\HotCommissionTool\IP.txt", "r") as f:
        for ip in f:
            ip = ip.strip()  # Remove newline characters
            commands.extend([
                f"python ModbusRW.py write {ip} 502 908 0",
                f"python ModbusRW.py write {ip} 502 908 1",
                f"python ModbusRW.py write {ip} 502 907 2"
            ])

    # Create queue for inter-thread communication
    q = queue.Queue()
    threads = []

    # Create and start threads
    for cmd in commands:
        thread = threading.Thread(target=modbus_rw_task, args=(q, cmd))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Collect results and write them to a file
    results = []
    while not q.empty():
        results.append(q.get().replace('[', '').replace(']', '').replace("'", ""))

    with open(file, "w") as f:
        f.write('\n'.join(results))  # Write results in one go for efficiency

if __name__ == "__main__":
    start = datetime.now()
    main()
    end = datetime.now()
    print(f"{start.strftime('%Y%m%d-%H%M%S')}: Data has been written to {file}, Total time: {end - start}")
