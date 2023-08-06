# ad_analyse_logs.py

import os
import json
import collections

def load_logs(filename):
    try:
        with open(os.path.join('logs', filename), 'r') as f:
            logs = json.load(f)
        return logs
    except FileNotFoundError:
        print(f"\nError: File {filename} does not exist.")
        sys.exit(1)

def correlate_same_process(logs1, logs2):
    # Group logs by process name
    log_dict1 = collections.defaultdict(list)
    for log in logs1:
        key = log['process']
        log_dict1[key].append(log)

    log_dict2 = collections.defaultdict(list)
    for log in logs2:
        key = log['process']
        log_dict2[key].append(log)

    # Find common keys in both dictionaries
    common_keys = set(log_dict1.keys()).intersection(log_dict2.keys())

    # Print correlated logs
    for key in common_keys:
        print(f"\nProcess: {key}")
        print("\nLog 1 Messages:")
        for log in log_dict1[key]:
            print(f"Timestamp: {log['month']} {log['day']} {log['time']}, Process: {log['process']}, Message: {log['message']}")
        print("\nLog 2 Messages:")
        for log in log_dict2[key]:
            print(f"Timestamp: {log['month']} {log['day']} {log['time']}, Process: {log['process']}, Message: {log['message']}")
        print("-----")

def correlate_same_host(logs1, logs2):
    # Group logs by host name
    log_dict1 = collections.defaultdict(list)
    for log in logs1:
        key = log['host']
        log_dict1[key].append(log)

    log_dict2 = collections.defaultdict(list)
    for log in logs2:
        key = log['host']
        log_dict2[key].append(log)

    # Find common keys in both dictionaries
    common_keys = set(log_dict1.keys()).intersection(log_dict2.keys())

    # Print correlated logs
    for key in common_keys:
        print(f"\nHost: {key}")
        print("\nLog 1 Messages:")
        for log in log_dict1[key]:
            print(f"Timestamp: {log['month']} {log['day']} {log['time']}, Process: {log['process']}, Message: {log['message']}")
        print("\nLog 2 Messages:")
        for log in log_dict2[key]:
            print(f"Timestamp: {log['month']} {log['day']} {log['time']}, Process: {log['process']}, Message: {log['message']}")
        print("-----")


def correlate_message_content(logs1, logs2):
    # Group logs by message content
    log_dict1 = collections.defaultdict(list)
    for log in logs1:
        key = log['message']
        log_dict1[key].append(log)

    log_dict2 = collections.defaultdict(list)
    for log in logs2:
        key = log['message']
        log_dict2[key].append(log)

    # Find common keys in both dictionaries
    common_keys = set(log_dict1.keys()).intersection(log_dict2.keys())

    # Print correlated logs
    for key in common_keys:
        print(f"\nMessage: {key}")
        print("\nLog 1 Messages:")
        for log in log_dict1[key]:
            print(f"Timestamp: {log['month']} {log['day']} {log['time']}, Process: {log['process']}, Message: {log['message']}")
        print("\nLog 2 Messages:")
        for log in log_dict2[key]:
            print(f"Timestamp: {log['month']} {log['day']} {log['time']}, Process: {log['process']}, Message: {log['message']}")
        print("-----")

def ad_analyse_logs():
    print("\nEnter the filenames of the two log files you want to correlate.")
    print("\n")
    while True:
        filename1 = input("Enter the filename of the first log file: ")
        if not os.path.exists(os.path.join('logs', filename1)):
            print(f"The file {filename1} does not exist. Please try again.")
            continue
        break

    while True:
        filename2 = input("Enter the filename of the second log file: ")
        if not os.path.exists(os.path.join('logs', filename2)):
            print(f"The file {filename2} does not exist. Please try again.")
            continue
        break

    logs1 = load_logs(filename1)
    logs2 = load_logs(filename2)

    print("\nSelect the type of correlation:")
    print("1. Same process, different timestamps")
    print("2. Same host, different processes")
    print("3. Based on message content")
    choice = input("\nEnter your choice: ")

    if choice == '1':
        correlate_same_process(logs1, logs2)
    elif choice == '2':
        correlate_same_host(logs1, logs2)
    elif choice == '3':
        correlate_message_content(logs1, logs2)
    else:
        print("Invalid choice.")
