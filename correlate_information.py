import os
import json

def correlate_information():

    print("\nCorrelate Gathered Network - Processes information")
    print("\nEnter both file names to begin (filename.json)\n")
    while True:
        network_file = input("Enter the name of the network file: ")
        # Check if files exist
        if os.path.exists(network_file):
            break
        else:
            print(f"Network file {network_file} does not exist. Please Check the file name.")

    while True:
        process_file = input("Enter the name of the process file: ")
        if os.path.exists(process_file):
            break
        else:
            print(f"Process file {process_file} does not exist. Please Check the file name")

    # Load the network information from the JSON file
    try:
        with open(network_file, 'r') as f:
            network_data = json.load(f)
    except Exception as e:
        print(f"An error occurred while reading the network file: {e}")
        return

    # Load the process information from the JSON file
    try:
        with open(process_file, 'r') as f:
            process_data = json.load(f)
    except Exception as e:
        print(f"An error occurred while reading the process file: {e}")
        return

    # Parse the network information into a dictionary keyed by PID
    network_info = {}
    for item in network_data:
        pid = item['PID']
        process_name = item['Process Name']
        family = item['Family']
        local_address = item['Local Address']
        remote_address = item['Remote Address']
        status = item['Status']
        network_info[pid] = (process_name, family, local_address, remote_address, status)

    # Parse the process information and correlate with the network information
    correlation_found = False
    for item in process_data:
        pid = item['PID']
        process_name = item['Process Name']
        username = item['Username']
        cpu_usage = item['CPU Usage']
        memory_usage = item['Memory Usage (MB)']
        status = item['Status']
        creation_time = item['Creation Time']

        # If the PID from the process information matches a PID in the network information, print the correlated information
        if pid in network_info:
            print(f"PID: {pid}")
            print(f"Process Name: {process_name}")
            print(f"Username: {username}")
            print(f"CPU Usage: {cpu_usage}")
            print(f"Memory Usage (MB): {memory_usage}")
            print(f"Process Status: {status}")
            print(f"Creation Time: {creation_time}")
            print(f"Network Process Name: {network_info[pid][0]}")
            print(f"Family: {network_info[pid][1]}")
            print(f"Local Address: {network_info[pid][2]}")
            print(f"Remote Address: {network_info[pid][3]}")
            print(f"Network Status: {network_info[pid][4]}")
            print("-----")
            correlation_found = True

    if not correlation_found:
        print("\nNo correlation found between the entered process and network information.")

