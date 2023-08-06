import psutil
import pwd
import datetime
import json

def running_processes():
    print("Gathering running processes...")
    processes = [proc for proc in psutil.process_iter(['pid', 'name', 'username', 'ppid', 'cpu_percent', 'memory_info', 'status', 'create_time'])]

    # First prompt asking on using filters and then following prompt if the answer is 'yes'
    while True:
        filter_choice = input("\nDo you want to add any filters like CPU/memory or filter by the user? (yes/no): ")
        if filter_choice.lower() not in ['yes', 'no']:
            print("Invalid input. Please enter 'yes' or 'no'.")
            continue
        if filter_choice.lower() == 'yes':
            while True:
                try:
                    min_cpu = input("Enter the minimum CPU usage (default: ALL): ")
                    min_cpu = float(min_cpu) if min_cpu else None
                    min_ram = input("Enter the minimum RAM usage in MB (default: ALL): ")
                    min_ram = float(min_ram) if min_ram else None
                    break
                except ValueError:
                    print("Invalid input. Please enter a number.")
            while True:
                user_filter = input("Enter the username to filter by (default: ALL): ")
                if user_filter:
                    if user_filter not in [user.pw_name for user in pwd.getpwall()]:
                        print("Invalid username. Please enter a valid username.")
                        continue
                else:
                    user_filter = None
                break
        else:
            min_cpu = None
            min_ram = None
            user_filter = None
        break

    # printing out the results with or without filters based on the choice in the first prompt
    details = []
    for proc in processes:
        cpu_usage = proc.info['cpu_percent']
        memory_usage = proc.info['memory_info'].rss / (1024 * 1024)  # convert to MB
        if (min_cpu is not None and cpu_usage < min_cpu) or (min_ram is not None and memory_usage < min_ram) or (user_filter is not None and proc.info['username'] != user_filter):
            continue
        create_time = datetime.datetime.fromtimestamp(proc.info['create_time']).strftime("%Y-%m-%d %H:%M:%S")
        detail = {
            "PID": proc.info['pid'],
            "Process Name": proc.info['name'],
            "Username": proc.info['username'],
            "CPU Usage": cpu_usage,
            "Memory Usage (MB)": memory_usage,
            "Status": proc.info['status'],
            "Creation Time": create_time
        }
        print(f"{proc.info['pid']:<10}{proc.info['name']:<35}{proc.info['username']:<15}{cpu_usage:<20.2f}{memory_usage:<25.2f}{proc.info['status']:<20}{create_time:<30}")
        details.append(detail)

    # Save option for the terminal output
    save = input("\nDo you want to save these details to a file? (yes/no): ")
    if save.lower() == 'yes':
        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"process_{timestamp_str}.json", 'w') as f:
            json.dump(details, f)
        print(f"Details saved to process_{timestamp_str}.json")

