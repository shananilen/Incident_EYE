# analyse_logs.py

import os
import json
import collections

def load_logs(filename):
    try:
        with open(os.path.join('logs', filename), 'r') as f:
            logs = json.load(f)
        return logs
    except FileNotFoundError:
        print(f"Error: File {filename} does not exist.")
        sys.exit(1)
        

def correlate_logs(logs1, logs2):
    # Create a dictionary where the key is a tuple (timestamp, host, process)
    # and the value is a list of log messages
    log_dict1 = collections.defaultdict(list)
    for log in logs1:
        key = (log['month'] + ' ' + log['day'] + ' ' + log['time'], log['host'], log['process'])
        log_dict1[key].append(log['message'])

    log_dict2 = collections.defaultdict(list)
    for log in logs2:
        key = (log['month'] + ' ' + log['day'] + ' ' + log['time'], log['host'], log['process'])
        log_dict2[key].append(log['message'])

    # Find common keys in both dictionaries
    common_keys = set(log_dict1.keys()).intersection(log_dict2.keys())

    # Print correlated logs
    for key in common_keys:
        print(f"Timestamp: {key[0]}")
        print(f"Host: {key[1]}")
        print(f"Process: {key[2]}")
        print(f"Log 1 Messages: {log_dict1[key]}")
        print(f"Log 2 Messages: {log_dict2[key]}")
        print("-----")

def analyse_logs():
    print("Enter the filenames of the two log files you want to correlate.")
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

    correlate_logs(logs1, logs2)
